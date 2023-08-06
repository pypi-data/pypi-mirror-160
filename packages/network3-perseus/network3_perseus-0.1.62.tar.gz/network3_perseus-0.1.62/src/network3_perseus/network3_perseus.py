import os
import yaml
import logging
import subprocess
from jinja2 import Environment, PackageLoader
from hedera import Client, AccountId, PrivateKey, Hbar, FileCreateTransaction, FileContentsQuery, FileId, FileAppendTransaction, FileInfoQuery

OPERATOR_ID= AccountId.fromString(os.environ["OPERATOR_ID"])
OPERATOR_PRIVATE_KEY= PrivateKey.fromString(os.environ["OPERATOR_PRIVATE_KEY"])
FILEID=os.environ["FILEID"]

class network3_perseus():
    def __init__(self):
        self.fileId=FILEID

    def configure_device(self):
        self.get_file_from_hedera()
        # self.add_file_to_hedera()
        # self.pre_change=self.capture_pre_state()
        # self.push_config(self.yaml_contents)
        # self.post_change=self.capture_post_state()

    def get_file_from_hedera(self):
        client = Client.forTestnet()
        client.setOperator(OPERATOR_ID, OPERATOR_PRIVATE_KEY)
        query = FileContentsQuery()
        hedera_fileId = FileId.fromString(self.fileId)
        contents = query.setFileId(hedera_fileId).execute(client)
        all_yaml = yaml.safe_load(contents.toStringUtf8())
        items=[]
        for item, value in all_yaml.items():
            items.append(item)
            print(max(items))
            print(item)
            print(value)

    def capture_pre_state(self):
        command="show running-config"
        self.output = subprocess.run(["python", "call_cli.py", command], capture_output=True)
        raw_json=self.output.stdout.decode('utf-8')
        print(raw_json)
        for line in raw_json.split('\n'):
            print(line)
            self.append_file_to_hedera(f"{ line } \n")
        query = FileInfoQuery().setFileId(self.fileId)
        info = query.execute(self.client)
        print("File size according to `FileInfoQuery`: ", info.size)

    def capture_post_state(self):
        command="show running-config"
        self.output = subprocess.run(["python", "call_cli.py", command], capture_output=True)
        raw_json=self.output.stdout.decode('utf-8')
        self.append_file_to_hedera("POST-CHANGE STATE")
        for line in raw_json.split('\n'):
            print(line)
            self.append_file_to_hedera(f"{ line } \n")
        query = FileInfoQuery().setFileId(self.fileId)
        info = query.execute(self.client)
        print("File size according to `FileInfoQuery`: ", info.size)

    def push_config(self,yaml_contents):
        env = Environment(loader=PackageLoader("network3_perseus", "templates"))
        intended_config_template = env.get_template('intended_config.j2')
        rendered_intended_config = intended_config_template.render(self.yaml_contents)
        subprocess.run(["python", "cli_configure.py", rendered_intended_config])

    def add_file_to_hedera(self):
        self.client = Client.forTestnet()
        self.client.setOperator(OPERATOR_ID, OPERATOR_PRIVATE_KEY)
        tran = FileCreateTransaction()
        fileContents = "PRE-CHANGE STATE"
        resp = tran.setKeys(OPERATOR_PRIVATE_KEY.getPublicKey()).setContents(fileContents).setMaxTransactionFee(Hbar(2)).execute(self.client)
        print("nodeId: ",  resp.nodeId.toString())
        self.nodeId = resp.nodeId.toString()
        receipt = resp.getReceipt(self.client)
        self.fileId = receipt.fileId
        query = FileInfoQuery().setFileId(self.fileId)
        info = query.execute(self.client)
        print("file: ",  self.fileId.toString())
        print("File size according to `FileInfoQuery`: ", info.size)
        
    def append_file_to_hedera(self, interface):
        tran = (FileAppendTransaction()
                .setFileId(self.fileId)
                .setContents(interface)
                .setMaxChunks(500)
                .setMaxTransactionFee(Hbar(2))
                .freezeWith(self.client))
        resp = tran.execute(self.client)
        self.receipt = resp.getReceipt(self.client)

def cli():
    invoke_class = network3_perseus()
    invoke_class.configure_device()

if __name__ == "__main__":
    cli()