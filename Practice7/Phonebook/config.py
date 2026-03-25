from configparser import ConfigParser
 
def load_config(filename = 'database.ini', section = 'postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for key, value in params:
            config[key] = value
    else:
        raise Exception(f"Section {section} is not found in the {filename} file.")
    
    return config

if __name__ == '__main__':
    print(load_config())

