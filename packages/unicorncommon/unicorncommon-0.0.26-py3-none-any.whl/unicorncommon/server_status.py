from enum import Enum

class SERVER_STATUS(Enum):
    OK                          = 0         # operation completed successfully
    INVALID_ACTION              = 1         # invalid action
    INVALID_REQUEST_SCHEMA      = 2         # request payload has does not comply with schema
    INTERNAL_ERROR              = 3         # internal errror, dev need to fix potential problems
    DATABASE_ERROR              = 4         # database operation failure for model update or creation

    INVALID_NODE_ID             = 5         # caller provided invalid task ID
    INVALID_APPLICATION_ID      = 6         # caller provided invalid applicaiton ID
    INVALID_TASK_ID             = 7         # caller provided invalid task ID
    INVALID_RUN_ID              = 8         # caller provided invalid run ID

    TASK_ALREADY_ACTIVE         = 9         # cannot set a run to a task as active since the task is already active
    TASK_ALREADY_INACTIVE       = 10        # cannot set a run to a task as inactive since the task is already inactive
    RUN_ALREADY_STOPPED         = 11
    LAUNCH_PROCESS_FAILED       = 12        # unable to spawn process for the desired application
    STOP_PROCESS_FAILED         = 13        # unable to send signal to a process
    NODE_IS_NOT_ACTIVE          = 14
    NODE_IS_NOT_UP              = 15


