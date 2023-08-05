"""DICOM protocol functions."""
# pylint: disable=global-statement
import logging
import typing as t

from fw_file.dicom import DICOMCollection
from pydicom.uid import ImplicitVRLittleEndian
from pynetdicom.ae import ApplicationEntity
from pynetdicom.association import Association
from pynetdicom.presentation import PresentationContext

# pylint: disable=no-name-in-module
from pynetdicom.sop_class import Verification  # type: ignore

from .parser import AEConfig

# pylint: enable=no-name-in-module

log = logging.getLogger(__name__)
# Supress association messages
logging.getLogger("pynetdicom.assoc").setLevel(logging.WARNING)

# Global association object
glob_association: t.Optional[Association] = None


def get_application_entity(
    ae_config: AEConfig,
) -> ApplicationEntity:
    """Get the ApplicationEntity.

    Args:
        ae_config (AEConfig): ApplicationEntity configuration.

    Returns:
        ApplicationEntity: pynetdicom ApplicationEntity
    """
    entity = ApplicationEntity(ae_title=ae_config.calling_ae)
    # Default 30s, expose as config option?
    # NOTE: ApplicationEntity does not accept these as args or kwargs
    # must add afterwards like here.
    entity.acse_timeout = 30
    entity.dimse_timeout = 30
    entity.network_timeout = 30
    return entity


def get_presentation_contexts(
    dcms: DICOMCollection, verification: bool
) -> t.List[PresentationContext]:
    """Get PresentationContexts from a DICOMCollection.

    Args:
        dcms (DICOMCollection): DICOMS
        verification (bool): If true, add Verification presentation context.

    Returns:
        t.List[PresentationContext]: PresentationContexts
    """
    # PresentationContext sometimes add ImplicitVRLittleEndian as a transfer
    # since that is the default, but doesn't always seem to, so we'll make sure
    # it is explicitely added here.
    transfer_syntaxes = list(
        set([*dcms.bulk_get("TransferSyntaxUID"), ImplicitVRLittleEndian])
    )
    sop_classes = list(set(dcms.bulk_get("SOPClassUID")))
    if verification:
        sop_classes.append(Verification)
    if len(sop_classes) > 128:
        raise RuntimeError("Too many presentation contexts.")
    presentation_contexts: t.List[PresentationContext] = []
    for sop_class in sop_classes:
        pres = PresentationContext()
        pres.abstract_syntax = sop_class
        pres.transfer_syntax = transfer_syntaxes
        presentation_contexts.append(pres)
    return presentation_contexts


def get_association(
    ae_config: AEConfig,
    dcms: DICOMCollection,
) -> Association:
    """Get association given AE and a collection of dicoms.

    Args:
        ae_config (AEConfig): ApplicationEntity configuration.
        dcms (DICOMCollection): Collection of dicoms to send.
            Needed to get correct presentation context.


    Raises:
        RuntimeError:
            - If too many presentation contexts.
            - If association fails.

    Returns:
        Association: _description_
    """
    entity = get_application_entity(ae_config)
    presentation_contexts = get_presentation_contexts(
        dcms, verification=(ae_config.tls.enabled if ae_config.tls else False)
    )
    entity.requested_contexts = presentation_contexts

    if ae_config.tls and ae_config.tls.enabled:
        ctx = ae_config.tls.get_ssl_context()
        association = entity.associate(
            ae_config.destination,
            ae_config.port,
            ae_title=ae_config.called_ae,
            tls_args=(ctx, ae_config.destination),
        )
    else:
        association = entity.associate(
            ae_config.destination, ae_config.port, ae_title=ae_config.called_ae
        )
    if not association.is_established:
        raise RuntimeError("Failed to establish AE association.")
    log.info("Successfully associated AE")
    # Release existing association, and populate global association
    global glob_association
    if glob_association:
        glob_association.release()
    glob_association = association
    return association


def release_association() -> None:
    """Release association."""
    global glob_association
    if glob_association:
        glob_association.release()
        glob_association = None
