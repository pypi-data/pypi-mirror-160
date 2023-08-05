import os
import yaml
import logging
import subprocess
from jinja2 import Environment, FileSystemLoader
from hedera import Client, AccountId, PrivateKey, Hbar, FileCreateTransaction, FileContentsQuery, FileId, FileAppendTransaction, FileInfoQuery

OPERATOR_ID= AccountId.fromString(os.environ["OPERATOR_ID"])
OPERATOR_PRIVATE_KEY= PrivateKey.fromString(os.environ["OPERATOR_PRIVATE_KEY"])
FILEID=os.environ["FILEID"]

class network3_perseus():
    def configure_device(self):
        self.get_file_from_hedera()
        self.add_file_to_hedera("PRE-CHANGE STATE")
        self.pre_change=self.capture_state()
        self.push_config(self.yaml_contents)
        self.post_change=self.capture_state()

    def get_file_from_hedera(self):
        client = Client.forTestnet()
        client.setOperator(OPERATOR_ID, OPERATOR_PRIVATE_KEY)
        query = FileContentsQuery()
        hedera_fileId = FileId.fromString(FILEID)
        contents = query.setFileId(hedera_fileId).execute(client)
        self.yaml_contents = yaml.safe_load(contents.toStringUtf8())
        return self.yaml_contents

    def capture_state(self):
        self.output = subprocess.run(["python", "call_cli.py", "show running-config"], capture_output=True)
        raw_json=self.output.stdout.decode('utf-8')
        for line in raw_json.split('\n'):
            print(line)
            self.append_file_to_hedera(f"{ line } \n")
        query = FileInfoQuery().setFileId(FILEID)
        info = query.execute(self.client)
        print("File size according to `FileInfoQuery`: ", info.size)

    def push_config(self,yaml_contents):
        template_dir = f'templates/cisco/nxos'
        env = Environment(loader=FileSystemLoader(template_dir))
        intended_config_template = env.get_template('intended_config.j2')
        rendered_intended_config = intended_config_template.render(yaml_contents)
        subprocess.run(["python", "cli_configure.py", rendered_intended_config])

    def add_file_to_hedera(self, raw_json):
        self.client = Client.forTestnet()
        self.client.setOperator(OPERATOR_ID, OPERATOR_PRIVATE_KEY)
        tran = FileCreateTransaction()
        fileContents = raw_json
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