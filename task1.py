# Fibonacci Series Generator
# Each number is the sum of the two preceding numbers
# F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)

def generate_fibonacci(n):
    """Generate a Fibonacci series of length n"""
    if n <= 0:
        print("Please enter a positive integer!")
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    else:
        series = [0, 1]
        for i in range(2, n):
            next_num = series[i-1] + series[i-2]
            series.append(next_num)
        return series

# --- main program ---
if __name__ == "__main__":
    # ask user input
    n = int(input("Enter how many terms you want in Fibonacci series: "))
    
    fib_series = generate_fibonacci(n)
    
    print(f"\nFibonacci series with {n} terms:")
    for num in fib_series:
        print(num, end=" ")
