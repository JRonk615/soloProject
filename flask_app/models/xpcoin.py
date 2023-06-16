
import time

class XPCoin:

    def __init__(self):

        self.earning = False
        self.hash_rate = 10000
        self.current_cap = 0
        self.supply_cap = 1000000000
        self.swap_rate = 1000000

    def earn_XPCoin(self):
        
        self.earning = True
        num_of_earns = 1000
        while True:

            print("Earning XPCoin")
            for i in range(num_of_earns):
                if i > 0:
                    time.sleep(1)
                if self.current_cap + self.hash_rate >= self.supply_cap:
                    print("XPCoin supply cap has been reached")
                    return False
                self.current_cap += self.hash_rate
                print(f'{self.current_cap}')
            

        return self


XPCoin = XPCoin()

XPCoin.earn_XPCoin()
