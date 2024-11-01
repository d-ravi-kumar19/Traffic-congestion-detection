import time
import sys

def processing_animation(duration=240):
        """Show a processing animation in the console.

        Args:
            duration (int): Duration in seconds for which the animation runs.
        """
        end_time = time.time() + duration
        while time.time() < end_time:
            for frame in "|/-\\":
                sys.stdout.write(f'\rProcessing... {frame}')
                sys.stdout.flush()
                time.sleep(0.1)
        sys.stdout.write('\rProcessing complete!      \n')
