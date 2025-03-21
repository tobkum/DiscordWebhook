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

    def Cleanup(self):
        del self.OnJobFinishedCallback
        del self.OnJobFailedCallback
        del self.OnJobSubmittedCallback
        del self.OnJobSuspendedCallback
        del self.OnJobResumedCallback
        del self.OnJobStartedCallback
        del self.OnJobErrorCallback

    def OnJobError(self, job, error, *args):
        discord_webhook_url = self.GetConfigEntry("DiscordWebhookURL")
        job_name = job.JobName
        user_name = job.JobUserName

        full_message = f":exclamation: Job error. **Error:** {error} **Job:** `{job_name}` **User:** `{user_name}`"

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

    def OnJobStarted(self, job):
        user_name = job.JobUserName
        self.send_discord_message(
            job, f":arrow_forward: Job started. **User:** `{user_name}`"
        )

    def OnJobSuspended(self, job):
        user_name = job.JobUserName
        self.send_discord_message(
            job, f":pause_button: Job suspended. **User:** `{user_name}`"
        )

    def OnJobResumed(self, job):
        user_name = job.JobUserName
        self.send_discord_message(
            job, f":arrow_forward: Job resumed. **User:** `{user_name}`"
        )

    def OnJobSubmitted(self, job):
        discord_webhook_url = self.GetConfigEntry("DiscordWebhookURL")
        job_name = job.JobName
        user_name = job.JobUserName

        full_message = (
            f":rocket: Job submitted. **Job:** `{job_name}` **User:** `{user_name}`"
        )

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

    def OnJobFinished(self, job):
        discord_webhook_url = self.GetConfigEntry("DiscordWebhookURL")
        job_name = job.JobName
        user_name = job.JobUserName
        start_time = job.JobStartedDateTime
        end_time = job.JobCompletedDateTime
        duration = end_time - start_time

        if len(job.JobOutputDirectories) > 0:
            output_path = job.JobOutputDirectories
            full_message = f":white_check_mark: Job finished. **Job:** `{job_name}` **User:** `{user_name}` **Duration:** `{duration}` **Output path:** `{output_path[0]}`"
        else:
            output_path = "Unknown"
            full_message = f":white_check_mark: Job finished. **Job:** `{job_name}` **User:** `{user_name}` **Duration:** `{duration}` **Output path:** `{output_path}`"

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

    def OnJobFailed(self, job):
        discord_webhook_url = self.GetConfigEntry("DiscordWebhookURL")
        job_name = job.JobName
        user_name = job.JobUserName

        full_message = f":x: Job failed. **Job:** `{job_name}` **User:** `{user_name}`"

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

    def send_discord_message(self, job, message):
        discord_webhook_url = self.GetConfigEntry("DiscordWebhookURL")
        job_name = job.JobName

        full_message = f"{message} **Job:** `{job_name}`"

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
