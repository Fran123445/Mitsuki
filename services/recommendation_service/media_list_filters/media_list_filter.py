
class MediaListFilter:

    def filter(self, media_list: list, params: dict):
        if not self.check_valid_params(params):
            return media_list

    def check_valid_params(self, params: dict):
        return True
        # I'm making it return true by default so each filter has to check for falsy cases
        # if they need it
