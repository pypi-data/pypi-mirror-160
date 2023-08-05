class HicPlatform(object):
    def create_campaign(self, campaign):
        raise NotImplementedError("Please Implement this method")

    def pause_campaign(self, campaign_id):
        raise NotImplementedError("Please Implement this method")

    def update_campaign(self, campaign):
        raise NotImplementedError("Please Implement this method")

    def get_account_performance(self, account_id):
        raise NotImplementedError("Please Implement this method")

    def get_ad_preview(self, job_id):
        raise NotImplementedError("Please Implement this method")

    def get_ad_manager_url(self, job_id):
        raise NotImplementedError("Please Implement this method")


class PlatformStatus:
    CREATING_QUEUE = "CREATING_QUEUE"
    CREATING = "CREATING"
    ACTIVE = "ACTIVE"
    CREATING_FAILED = "CREATING_FAILED"
    PAUSED = "PAUSED"
    PAUSING = "PAUSING"
    PAUSING_QUEUE = "PAUSING_QUEUE"
    PAUSING_FAILED = "PAUSING_FAILED"
