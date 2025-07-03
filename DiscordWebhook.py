import Deadline.Events as DeadlineEvents
import requests
import json


def GetDeadlineEventListener():
    return DiscordWebhookEventListener()


def CleanupDeadlineEventListener(deadlinePlugin):
    deadlinePlugin.Cleanup()


class DiscordWebhookEventListener(DeadlineEvents.DeadlineEventListener):

    def __init__(self):
        super().__init__()
        self.OnJobFinishedCallback += self.OnJobFinished
        self.OnJobFailedCallback += self.OnJobFailed
        self.OnJobSubmittedCallback += self.OnJobSubmitted
        self.OnJobSuspendedCallback += self.OnJobSuspended
        self.OnJobResumedCallback += self.OnJobResumed
        self.OnJobStartedCallback += self.OnJobStarted
        self.OnJobErrorCallback += self.OnJobError
        self.OnJobErrorCallback += self.OnJobDeleted

    def Cleanup(self):
        del self.OnJobFinishedCallback
        del self.OnJobFailedCallback
        del self.OnJobSubmittedCallback
        del self.OnJobSuspendedCallback
        del self.OnJobResumedCallback
        del self.OnJobStartedCallback
        del self.OnJobErrorCallback
        del self.OnJobDeleted

    def OnJobError(self, job, error, *args):
        message = f":exclamation: Job error. **Error:** {error}"
        self.send_discord_message(job, message)

    def OnJobStarted(self, job):
        message = ":arrow_forward: Job started."
        self.send_discord_message(job, message)

    def OnJobSuspended(self, job):
        message = ":pause_button: Job suspended."
        self.send_discord_message(job, message)

    def OnJobResumed(self, job):
        message = ":arrow_forward: Job resumed."
        self.send_discord_message(job, message)

    def OnJobSubmitted(self, job):
        message = ":rocket: Job submitted."
        self.send_discord_message(job, message)

    def OnJobFinished(self, job):
        start_time = job.JobStartedDateTime
        end_time = job.JobCompletedDateTime
        duration = end_time - start_time

        if len(job.JobOutputDirectories) > 0:
            output_path = job.JobOutputDirectories
            message = f":white_check_mark: Job finished. **Duration:** `{duration}` **Output path:** `{output_path[0]}`"
        else:
            output_path = "Unknown"
            message = f":white_check_mark: Job finished. **Duration:** `{duration}` **Output path:** `{output_path}`"
        self.send_discord_message(job, message)

    def OnJobFailed(self, job):
        message = ":x: Job failed."
        self.send_discord_message(job, message)

    def OnJobDeleted(self, job):
        message = ":scream: Job deleted."
        self.send_discord_message(job, message)

    def send_discord_message(self, job, message):
        discord_webhook_url = self.GetConfigEntry("DiscordWebhookURL")
        job_name = job.JobName
        user_name = job.JobUserName

        full_message = f"{message} **Job:** `{job_name}` **User:** `{user_name}`"

        data = {"content": full_message}
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            discord_webhook_url, data=json.dumps(data), headers=headers
        )
        if response.status_code != 204:
            self.LogWarning(
                "Failed to send Discord message. Status code: "
                + str(response.status_code)
            )