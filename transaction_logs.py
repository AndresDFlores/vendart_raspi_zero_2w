import json
from pathlib import Path

class TransactionLogger:


    def __init__(self, filename: str):
        self.filename = filename



    def get_transaction_details(self, transaction_record_dict:dict):

        self.transaction_id = transaction_record_dict["data"]["id"]
        self.status = transaction_record_dict["data"]["object"]["payment"]["status"]

        details_dict = {
            "transaction_id": transaction_record_dict["data"]["id"],
            "created_at": transaction_record_dict["created_at"],
            "status": transaction_record_dict["data"]["object"]["payment"]["status"],
            "customer":{
                "first_name": transaction_record_dict["data"]["object"]["payment"]["billing_address"]["first_name"],
                "last_name": transaction_record_dict["data"]["object"]["payment"]["billing_address"]["last_name"],
                "email_address": transaction_record_dict["data"]["object"]["payment"]["buyer_email_address"]
            },
            "meta":{
                "merchant_id": transaction_record_dict["merchant_id"],
                "event_id": transaction_record_dict["event_id"],
                "application_id": transaction_record_dict["data"]["object"]["payment"]["application_details"]["application_id"],
                "square_product": transaction_record_dict["data"]["object"]["payment"]["application_details"]["square_product"],
                "location_id": transaction_record_dict["data"]["object"]["payment"]["location_id"]
            },
            "order":{
                "order_id": transaction_record_dict["data"]["object"]["payment"]["order_id"],
                "total_paid": transaction_record_dict["data"]["object"]["payment"]["total_money"]["amount"],
                "currency_paid": transaction_record_dict["data"]["object"]["payment"]["total_money"]["currency"],
                "source_type": transaction_record_dict["data"]["object"]["payment"]["source_type"],
                "receipt_number": transaction_record_dict["data"]["object"]["payment"]["receipt_number"]
            }
        }

        return details_dict
    


    def extract_transaction_ids(self):
        transaction_ids = []

        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                record = json.loads(line)

                transaction_id = record["transaction_id"]
                transaction_ids.append(transaction_id)

        return transaction_ids
    


    def create_jsonl_file(self):
        path = Path(self.filename)
        if not path.exists():
            path.touch()



    def write_jsonl_data(self, data: dict):
        path = Path(self.filename)


        # Append the dictionary as a JSON object on its own line
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")



    def read_jsonl_data(self):
        path = Path(self.filename)
        records = []

        if not path.exists():
            return records  # empty list if file doesn't exist

        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:  # skip blank lines
                    records.append(json.loads(line))

        return records



    def main(self, transaction_record_dict:dict):

        data_to_write = self.get_transaction_details(transaction_record_dict)

        self.create_jsonl_file()
        ids = self.extract_transaction_ids()

        if self.transaction_id not in ids and self.status == "COMPLETED":
            self.write_jsonl_data(data_to_write)
            self.publish_to_udp=True
        else:
            self.publish_to_udp=False

