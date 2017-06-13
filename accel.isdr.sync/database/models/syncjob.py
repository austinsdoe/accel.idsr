
class SyncJob():
    """
    Class that represents SyncJob objects will behave like a logger.
    """
    def __init__(self, log_time, status, message, content_type):
        """
        Initializes the SyncJob object
        :param log_time: Time log inserted
        :type log_time: Datetime
        :param status: Success or Fail
        :type status: String
        :param message: Log message.
        :type message: String
        :param content_type: Content type that log occured while updating
        :type content_type: String
        """
        self.log_time = log_time
        self.status = status
        self.message = message
        self.content_type = content_type

    def get_log_time(self):
        return self.log_time

    def get_status(self):
        return self.status

    def get_message(self):
        return self.message

    def get_content_type(self):
        return self.content_type

    def set_idsr_id(self, idsr_id):
        self.idsr_id = idsr_id

    def set_idsr_code(self, idsr_code):
        self.idsr_code = idsr_code

    def get_db_format(self):
        result = {
            'log_time': self.log_time.strftime('%d/%m/%Y %M:%S'),
            'status': self.status,
            'message': self.message,
            'content_type': self.content_type
        }
        if hasattr(self, "idsr_id"):
            result['idsr_form_id'] = self.idsr_id
        if hasattr(self, "idsr_code"):
            result['idsr_form_code'] = self.idsr_code
        return result
