from zengin_code import Bank

def get_bank_list():
    bank_list = [(code, Bank[code].name) for code in Bank.all]
    return bank_list

def get_branch_list(bank_code):
    branch_list = []
    try:
        branches = Bank[bank_code].branches
        branch_list = [(code, branch.name) for code, branch in branches.items()]
    except:
        pass
    return branch_list
