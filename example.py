from cfg import ConfigManager

# Example usage
if __name__ == "__main__":
    config = ConfigManager.register("example")
    if config:
        config.example.name = "Foo"
        config.api.value = "Bar"
        config.example.value = 69
        config.api.abc = None
        print(config.example.name)  # Output: 37
        print(config.example.value)  # Output: 37
        print(config.api.value)      # Output: Bar
        print(config.api.abc)
        if config.api.abc is None:
            print("I am None")
        else:
            print("I am Some")
    else:
        print("Failed to register config.")