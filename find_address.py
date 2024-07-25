import pyvisa

def main():
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()
    print(f"Connected resources:")
    for resource in resources:
        try:
            inst = rm.open_resource(resource)
            response = inst.read()
            print(f"Device at {resource} is {response}")
            inst.close()
        except:
            print(f"Couldn't communicate w/ {resource}")

if __name__ == "__main__":
    main()