import redis
import csv

def get_redis_info(host, port, password, db_index=None):
    try:
        # Connect to the Redis instance and select the specified database
        if db_index is not None:
            r = redis.StrictRedis(host=host, port=port, password=password, db=db_index, decode_responses=True)
        else:
            r = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        
        # Get the INFO output
        info = r.info()
        
        # Extract required information
        used_memory_peak_human = info.get('used_memory_peak_human', 'N/A')
        instantaneous_ops_per_sec = info.get('instantaneous_ops_per_sec', 'N/A')
        
        return used_memory_peak_human, instantaneous_ops_per_sec
    except Exception as e:
        print(f"Error connecting to Redis at {host}:{port} - {str(e)}")
        return 'N/A', 'N/A'

def main(input_file, output_file):
    results = []
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        # Skip empty lines and comments
        if line.strip() == '' or line.strip().startswith('#'):
            continue
        
        # Parse connection details
        parts = line.strip().split(':')
        if len(parts) < 4:
            print(f"Skipping improperly formatted line: {line.strip()}")
            continue
        
        host = parts[0]
        port = int(parts[1])
        password = parts[2] if parts[2] != '' else None
        instance_name = parts[3]
        
        # Check if Redis Enterprise (using DNS name)
        if '_RE_' in instance_name.upper():
            try:
                used_memory_peak_human, instantaneous_ops_per_sec = get_redis_info(host, port, password)
            except IndexError:
                print(f"Skipping improperly formatted instance name or db_index: {line.strip()}")
                continue
        else:
            # Assume Redis OSS format (without db_index)
            used_memory_peak_human, instantaneous_ops_per_sec = get_redis_info(host, port, password)
        
        # Construct a descriptive name for the output
        name = f"{instance_name}"
        
        # Append result
        results.append((name, used_memory_peak_human, instantaneous_ops_per_sec))
    
    # Write the results to the output file
    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Redis Instance', 'Used Memory Peak (Human)', 'Instantaneous Ops Per Sec'])
        writer.writerows(results)

if __name__ == "__main__":
    input_file = 'redis_connections.txt'  # Input file with connection details
    output_file = 'redis_info_output.txt'  # Output file with collected information
    main(input_file, output_file)
