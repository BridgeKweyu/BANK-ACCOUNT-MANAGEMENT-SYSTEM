class BankAccount:
    """
    A bank account class demonstrating encapsulation, property decorators,
    validation, and transaction history.
    """
    def __init__(self, acc_num: str, holder: str, initial_balance: float = 0.0):
        """
        Initialize a new bank account.
        Args:
            acc_num: Account number (read-only after creation)
            holder: Name of account holder
            initial_balance: Starting balance (default 0.0)
        """
        self.__account_number = acc_num      
        self.__account_holder = holder       
        self.__balance = 0.0                 
        self.__transaction_history = []      
        self.__overdraft_protection = False  

        self.balance = initial_balance

        if initial_balance > 0:
            self.__log_transaction("Initial deposit", initial_balance)

    @property
    def account_number(self) -> str:
        """Read-only property for account number."""
        return self.__account_number

    @property
    def balance(self) -> float:
        """Get current balance."""
        return self.__balance

    @balance.setter
    def balance(self, amount: float):
        """
        Set balance with validation (no negative balances).
        Args:
            amount: New balance amount
        Raises:
            ValueError: If amount is negative
        """
        if amount < 0:
            raise ValueError("Balance cannot be negative.")
        self.__balance = amount

    def deposit(self, amount: float) -> bool:
        """
        Deposit money into the account.
        Args:
            amount: Amount to deposit (must be positive)
        Returns:
            bool: True if deposit successful
        Raises:
            ValueError: If amount <= 0
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        self.__balance += amount
        self.__log_transaction("Deposit", amount)
        return True

    def withdraw(self, amount: float) -> bool:
        """
        Withdraw money from the account.
        Args:
            amount: Amount to withdraw
        Returns:
            bool: True if withdrawal successful
        Raises:
            ValueError: If amount <= 0 or amount exceeds balance
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        if amount > self.__balance:
            if self.__overdraft_protection:
                raise ValueError(
                    f"Insufficient funds. Overdraft protection enabled. "
                    f"Balance: {self.__balance:.2f}"
                )
            else:
                raise ValueError(
                    f"Insufficient funds. Balance: {self.__balance:.2f}, "
                    f"Requested: {amount:.2f}"
                )
        self.__balance -= amount
        self.__log_transaction("Withdrawal", -amount)
        return True

    def get_balance(self) -> float:
        """Public method to get current balance."""
        return self.__balance

    def display_account_info(self) -> None:
        """Display account details in a readable format."""
        print("=" * 40)
        print(f"Account Number: {self.__account_number}")
        print(f"Account Holder: {self.__account_holder}")
        print(f"Current Balance: Ksh{self.__balance:.2f}")
        print(f"Overdraft Protection: {'Enabled' if self.__overdraft_protection else 'Disabled'}")
        print("=" * 40)

    def __log_transaction(self, transaction_type: str, amount: float) -> None:
        """
        Private method to log each transaction.
        Args:
            transaction_type: Type of transaction (Deposit/Withdrawal/etc.)
            amount: Transaction amount (positive for deposit, negative for withdrawal)
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__transaction_history.append({
            "date": timestamp,
            "type": transaction_type,
            "amount": amount,
            "balance_after": self.__balance
        })

    def get_transaction_history(self) -> list:
        """
        Return a copy of transaction history (read-only access).
        Returns:
            list: List of transaction dictionaries
        """
        return self.__transaction_history.copy()

    def print_transaction_history(self) -> None:
        """Print formatted transaction history."""
        if not self.__transaction_history:
            print("No transactions yet.")
            return
        print("\n" + "=" * 60)
        print(f"Transaction History for Account {self.__account_number}")
        print("=" * 60)
        for txn in self.__transaction_history:
            amount_str = f"+Ksh{txn['amount']:.2f}" if txn['amount'] > 0 else f"-Ksh{abs(txn['amount']):.2f}"
            print(f"{txn['date']} | {txn['type']:12} | {amount_str:8} | Balance: Ksh{txn['balance_after']:.2f}")
        print("=" * 60)

    def enable_overdraft_protection(self) -> None:
        """Enable overdraft protection."""
        self.__overdraft_protection = True
        print("Overdraft protection enabled.")

    def disable_overdraft_protection(self) -> None:
        """Disable overdraft protection."""
        self.__overdraft_protection = False
        print("Overdraft protection disabled.")

    def calculate_interest(self, annual_rate: float, years: float = 1) -> float:
        """
        Calculate compound interest on current balance.
        Args:
            annual_rate: Annual interest rate (e.g., 0.05 for 5%)
            years: Number of years to calculate interest for
        Returns:
            float: Interest amount (simple interest for simplicity)
        """
        if annual_rate < 0:
            raise ValueError("Interest rate cannot be negative.")
        interest = self.__balance * annual_rate * years
        return round(interest, 2)

class SavingsAccount(BankAccount):
    """
    SavingsAccount subclass with interest rate and minimum balance requirements.
    """
    def __init__(self, acc_num: str, holder: str, initial_balance: float = 0.0, interest_rate: float = 0.02):
        """
        Initialize a savings account.
        Args:
            acc_num: Account number
            holder: Account holder name
            initial_balance: Starting balance
            interest_rate: Annual interest rate (default 2%)
        """
        super().__init__(acc_num, holder, initial_balance)
        self.__interest_rate = interest_rate
        self.__minimum_balance = 100.0

        if initial_balance < self.__minimum_balance:
            print(f"Warning: Savings accounts require minimum balance of Ksh{self.__minimum_balance:.2f}")
    @property
    def interest_rate(self) -> float:
        """Get current interest rate."""
        return self.__interest_rate
    @interest_rate.setter
    def interest_rate(self, rate: float):
        """Set interest rate with validation."""
        if rate < 0:
            raise ValueError("Interest rate cannot be negative.")
        self.__interest_rate = rate

    def apply_interest(self) -> None:
        """
        Apply annual interest to the account balance.
        """
        interest = self.calculate_interest(self.__interest_rate, 1)
        self.deposit(interest)
        self._BankAccount__log_transaction("Interest Applied", interest)
        print(f"Interest of Ksh{interest:.2f} applied at {self.__interest_rate * 100}% APR.")

    def withdraw(self, amount: float) -> bool:
        """
        Override withdraw to enforce minimum balance for savings accounts.
        """
        if self.get_balance() - amount < self.__minimum_balance:
            raise ValueError(
                f"Withdrawal denied. Savings account must maintain minimum balance of "
                f"Ksh{self.__minimum_balance:.2f}. Current balance: Ksh{self.get_balance():.2f}"
            )
        return super().withdraw(amount)

    def display_account_info(self) -> None:
        """Override to include interest rate information."""
        super().display_account_info()
        print(f"Account Type: Savings")
        print(f"Interest Rate: {self.__interest_rate * 100:.2f}%")
        print(f"Minimum Balance: Ksh{self.__minimum_balance:.2f}")

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING BASIC BANK ACCOUNT")
    print("=" * 60)

    acc1 = BankAccount("123456789", "Bridge Kweyu", 500.00)
    acc1.display_account_info()

    acc1.deposit(150.00)
    print(f"After deposit: Ksh{acc1.get_balance():.2f}")

    acc1.withdraw(200.00)
    print(f"After withdrawal: Ksh{acc1.get_balance():.2f}")

    try:
        acc1.deposit(-50)
    except ValueError as e:
        print(f"Error caught: {e}")

    try:
        acc1.withdraw(1000)
    except ValueError as e:
        print(f"Error caught: {e}")

    acc1.print_transaction_history()

    # Test interest calculation
    interest = acc1.calculate_interest(0.05, 1)
    print(f"5% interest on Ksh{acc1.get_balance():.2f} for 1 year: Ksh{interest:.2f}")

    print("\n" + "=" * 60)
    print("TESTING SAVINGS ACCOUNT")
    print("=" * 60)

    sav1 = SavingsAccount("SAV987654", "Allan Mara", 500.00, 0.03)
    sav1.display_account_info()

    sav1.apply_interest()
    sav1.display_account_info()

    try:
        sav1.withdraw(450)
    except ValueError as e:
        print(f"Error caught: {e}")

    print(f"\nAccount number (read-only): {acc1.account_number}")