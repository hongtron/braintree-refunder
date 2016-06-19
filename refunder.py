import input_helper
import file_parser
import logger
import braintree
import sys


class Refunder:
    def __init__(self):
        self.input_helper = input_helper.InputHelper()
        self.logger = None
        self.preview_line = None
        self.file_parser = None
        self.id_index = None
        self.has_headers = None
        self.full_refund = None
        self.refund_amount_index = None
        self.braintree = braintree

    def setup(self):
        input_file = self.input_helper.get_file()
        self.file_parser = file_parser.FileParser(input_file)
        self.logger = logger.Logger(input_file.replace('.csv', '.log'))
        self.preview_line = self.file_parser.advance()
        self.id_index = self.input_helper.confirm_column(self.preview_line, "transaction IDs")
        self.has_headers = self.input_helper.yes_no("Is the first value a header?")
        self.full_refund = self.input_helper.yes_no("Should the full amount be refunded?")
        if not self.full_refund:
            self.refund_amount_index = self.input_helper.confirm_column(self.preview_line, "refund amounts")
        merchant_id = self.input_helper.get_value("Merchant ID? ")
        public_key = self.input_helper.get_value("Public key? ")
        private_key = self.input_helper.get_value("Private key? ")
        if self.input_helper.yes_no("Production?"):
            environment = braintree.Environment.Production
        else:
            environment = braintree.Environment.Sandbox
        self.braintree.Configuration.configure(environment, merchant_id, public_key, private_key)

    def refund(self):
        current_row = self.preview_line
        if self.has_headers:
            current_row = self.file_parser.advance()
        counter = 0
        while current_row:
            counter += 1
            if counter % 10 == 0:
                sys.stderr.write('.')
            if self.full_refund:
                refund_amount = ''
            else:
                refund_amount = current_row[self.refund_amount_index]
            self._refund_transaction(current_row[self.id_index], refund_amount)
            current_row = self.file_parser.advance()
        self.logger.close()

    def _refund_transaction(self, txn_id, refund_amount):
        if refund_amount == '':
            result = self.braintree.Transaction.refund(txn_id)
        else:
            result = self.braintree.Transaction.refund(txn_id, refund_amount)
        self.logger.log_result(txn_id, result)


def main():
    refunder = Refunder()
    refunder.setup()
    refunder.refund()
    print "Done! Check log for errors."


main()
