from enum import Enum


class SlotCommand(str, Enum):
    UNPAUSE = 'unpause'
    PAUSE = 'pause'
    FINISH = 'finish'
    ON_IDLE = 'on_idle'
    ALWAYS_ON = 'always_on'


class ClientOption(str, Enum):
    # Taken from FAHControl.glade _option parsing made in old client, in order of appearance.
    USER = 'user-option'
    TEAM = 'team-option'
    PASSKEY = 'passkey-option'
    PASSWORD = 'password-option'
    COMMAND_PORT = 'command-port-option'
    ALLOW = 'allow-option'
    DENY = 'deny-option'
    COMMAND_ALLOW_NO_PASS = 'command-allow-no-pass-option'
    COMMAND_DENY_NO_PASS = 'command-deny-no-pass-option'

    PROXY_ENABLE = 'proxy-enable-option'
    PROXY = 'proxy-option'
    PROXY_PASS = 'proxy-pass-option'
    PROXY_USER = 'proxy-user-option'

    CAUSE = 'cause-option'
    CORE_PRIORITY = 'core-priority-option'
    CPU_USAGE = 'cpu-usage-option'
    GPU_USAGE = 'gpu-usage-option'
    CHECKPOINT = 'checkpoint-option'
    NO_ASSEMBLY = 'no-assembly-option'
    PAUSE_ON_BATTERY = 'pause-on-battery-option'
    GPU_INDEX = 'gpu-index-option'
    OPENCL_INDEX = 'opencl-index-option'
    CUDA_INDEX ='cuda-index-option'
    POWER = 'power'


class ClientProtocol(object):
    @property
    def option_names(self):
        co: Enum
        return [co.value for co in ClientOption]

    @property
    def inactive_commands(self):
        return [
            'updates clear',
            'updates add 0 4 $heartbeat',
            'updates add 1 5 $ppd',
        ]

    @property
    def active_commands(self):
        return self.inactive_commands + [
            'updates add 2 1 $(options %s *)' % ' '.join(self.option_names),
            'updates add 3 4 $queue-info',
            'updates add 4 1 $slot-info',
            'info',
            'log-updates start',
            'configured',
        ]

    @staticmethod
    def auth_command(password):
        return f'auth "{password}"'
