primes = []

for num in range(1, 251):
    if num > 1:
        is_prime = True
        for i in range(2, num):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)

with open("results.txt", "w") as f:
    for p in primes:
        f.write(str(p) + "\n")

print("Prime numbers saved to results.txt")

