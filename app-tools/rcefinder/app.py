#!/usr/bin/env python3
import arguably
import subprocess
import os
import pwn

pwn.context.log_level = 'debug'

class Run:
    def __init__(self, target, rulesDir):
        self.binary = "semgrep"
        self.listRules  = rulesDir
        self.target = target
        
    def rules(self):
        for rules in os.listdir(self.listRules):
            pwn.log.info(f'using rules : {rules}')

    def check(self):
        if not os.path.isfile(self.target):
            if os.path.exists(self.target):
                
                for files in os.listdir(self.target):
                    pwn.log.info(f'scanning {files}')
                # os.chdir(self.target)
                # self.target = ""
        
            
    def start(self):
        self.rules()  
        self.check()
        subprocess.run(["semgrep","scan",self.target,"--config", self.listRules, '--text', '--output', f'{self.target}.txt'])
        pwn.log.success(f'done scanning and the results in {self.target}.txt')

@arguably.command
def start(target, rules="./rules"):
    """
    Welcome to rceFinder, this tools to findign an specific code to finding an Remote Code Execution.
    Args:
        target: a target folder to test if its vuln or not
        rules: rules folder
    """
    Run(target=target,rulesDir=rules).start()

        


if __name__ == "__main__":
    arguably.run()


