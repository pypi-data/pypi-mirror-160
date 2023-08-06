from firstsdk.shipments import get_shipments_rates

def main():
    rates = get_shipments_rates()
    print(rates)

if __name__ == '__main__':
    main()