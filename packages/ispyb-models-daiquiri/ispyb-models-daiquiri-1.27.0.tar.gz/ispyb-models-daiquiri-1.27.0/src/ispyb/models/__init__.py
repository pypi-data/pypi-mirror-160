from sqlalchemy.orm import relationship

from ._auto_db_schema import *  # noqa F403
from ._auto_db_schema import AutoProcProgram, AutoProcScaling, ProcessingJob, UserGroup

__version__ = "1.27.0"


AutoProcProgram.AutoProcProgramAttachments = relationship(
    "AutoProcProgramAttachment", back_populates="AutoProcProgram"
)
AutoProcScaling.AutoProcScalingStatistics = relationship(
    "AutoProcScalingStatistics", back_populates="AutoProcScaling"
)
ProcessingJob.ProcessingJobParameters = relationship(
    "ProcessingJobParameter", back_populates="ProcessingJob"
)
ProcessingJob.ProcessingJobImageSweeps = relationship(
    "ProcessingJobImageSweep", back_populates="ProcessingJob"
)
UserGroup.Permission = relationship(
    "Permission", secondary="UserGroup_has_Permission", back_populates="UserGroup"
)
