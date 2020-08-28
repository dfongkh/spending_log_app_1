class Category:

    def __init__(self, category):
        self.category = category
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
    
    def withdraw(self, amount, description=""):
        if self.check_funds(amount) == True:
            self.ledger.append({"amount": amount*-1, "description": description})
            return True
        else: return False

    def get_balance(self):
        balance = 0
        for i in range(len(self.ledger)):
            balance += self.ledger[i]["amount"]
        return balance

    def transfer(self, amount, new_category):
        if self.check_funds(amount) == True:
            self.ledger.append({"amount": amount*-1, "description": f"Transfer to {new_category.category}"})
            new_category.ledger.append({"amount": amount, "description": f"Transfer from {self.category}"})
            return True
        else: return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def total_spending(self):
        spending = 0
        for transaction in self.ledger:
            if transaction["amount"] < 0 and transaction["description"][:11] != "Transfer to":
                spending += transaction["amount"]*-1
        return spending

    def __str__(self):
        remain_space = 30-len(self.category)
        if remain_space % 2 == 0:
            star = "*" * (remain_space//2)
            output = f"{star}{self.category}{star}"
        else:
            l_star = "*"*(remain_space//2)
            r_star = "*"+l_star
            output = f"{l_star}{self.category}{r_star}"

        for i in range(len(self.ledger)):
            descp = self.ledger[i]["description"][:23]
            amount = self.ledger[i]["amount"]
            output += f"\n{descp:23}{amount:7.2f}"
        
        output += f"\nTotal: {self.get_balance():.2f}"
        return output

def create_spend_chart(categories):
    spending_list = []
    cat_list = []
    for each_cat in categories:
        cat_list.append(each_cat.category)
        spending_list.append(each_cat.total_spending())
    total = sum(spending_list)
    for i in range(len(spending_list)):
        spending_list[i]= int(spending_list[i] / total * 10)*10

    output = "Percentage spent by category"
    for i in range(100,-10,-10):
        output += f"\n{i:3}| "
        for x in spending_list:
            if i <= x:
                output += "o  "
            else: output += "   "
    output += "\n    " + "-"*(len(spending_list)*3+1)
    max_len = max(len(x) for x in cat_list)
    for i in range(max_len):   
        output += "\n     "
        for column in cat_list:              
            if i < len(column):
                output += column[i] + "  "
            else:
                output += "   "
    return output



food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
print(food.get_balance())
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)

print(food)
print(clothing)
print(auto)
print(create_spend_chart([clothing, food, auto]))
