import csv


class Logger:
    def __init__(self, log_file):
        self.log = open(log_file, 'w')
        self.writer = csv.DictWriter(
            self.log,
            ['Original Txn ID', 'Refund Txn ID', 'Error Message']
        )
        self.writer.writeheader()

    def log_result(self, original_id, result):
    	if result.is_success:
            self.writer.writerow({'Original Txn ID': original_id, 'Refund Txn ID': result.transaction.id, 'Error Message': ''})
    	else:
            self.writer.writerow({'Original Txn ID': original_id, 'Refund Txn ID': '', 'Error Message': result.message})

    def close(self):
        self.log.close()
