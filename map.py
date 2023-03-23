from flask import Flask, request, jsonify

app = Flask(__name__)

def flatten_dict(d, parent_key='', sep='.', array_type='full'):
    """
    Flatten a dictionary object by converting nested keys into dot-separated keys.

    :param d: The dictionary to be flattened.
    :param parent_key: The string key of the parent dictionary, if any.
    :param sep: The separator string used to separate key names in the resulting flattened keys.
    :param array_type: The type of array notation to use. 'full' retains all array indexes, 'simple' reduces all indexes to 0.
    :return: A dictionary with all keys flattened.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep, array_type=array_type).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, f"{new_key}{sep}{i}", sep=sep, array_type=array_type).items())
                else:
                    if array_type == 'simple':
                        new_key = new_key.replace(f".{i}", '.0')
                    items.append((f"{new_key}{sep}{i}", item))
        else:
            items.append((new_key, v))
    if array_type == 'simple':
        items = list(set([item if not item[0].endswith('.0') else (item[0].replace('.0', '.0.0'), item[1]) for item in items]))
    return dict(items)


@app.route('/headers', methods=['POST'])
def headers():
    data = request.get_json()
    headers = data[0]
    array_type = request.args.get('array', 'full')
    flat_headers = flatten_dict(headers, array_type=array_type)
    return jsonify(list(flat_headers.keys()))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8084)
