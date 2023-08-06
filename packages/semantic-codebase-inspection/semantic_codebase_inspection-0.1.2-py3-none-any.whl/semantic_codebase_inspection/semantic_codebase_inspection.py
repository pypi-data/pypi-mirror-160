import tensorflow_text
import tensorflow_hub as hub
import inspect
print("Importing modules and semantic model.")


def load_model():
    print('loading model')
    return hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3")


def calc_dist(a, b):
    total = 0
    for i in range(len(a)):
        total += (a[i] - b[i])**2
    return total ** 0.5


defaults_to_block = set([
    '__builtins__',
    'inspect',
    'nlp',
    'recusively_construct_list_of_objects_from_object',
    'get_string_of_class_from_object',
    '__name__',
    '__doc__',
    '__package__',
    '__loader__',
    '__spec__',
    '__annotations__',
    '__file__',
    '__cached__',
    'defaults_to_block',
    'search_dict_of_everything_for_sentence',
    'recusively_construct_dict_of_all_objects_from_object',
    'parse_text_into_sentence_for_vectorization',
    'display_semantic_candidates',
    'run_semantic_search_through_program'
])


def parse_text_into_sentence_for_vectorization(text):
    acceptable_chararacters = 'abcdefghijklmnopqrstuvwxyz'
    acceptable_chararacters += acceptable_chararacters.upper() + ' '
    acceptable_chararacters_set = set(acceptable_chararacters)
    output = ''
    for character in text:
        if character in acceptable_chararacters_set:
            output += character
        else:
            output += ' '
    return output


def get_string_of_class_from_object(object_to_examine):
    string = str(type(object_to_examine))
    return ' ' + string[8:-2] + ' '


def recusively_construct_dict_of_all_objects_from_object(module_to_explore=None, recursion_floor=10, set_to_block_repeats=defaults_to_block):
    if not recursion_floor:
        return {}
    iterable_of_objects_to_explore = inspect.getmembers(module_to_explore)
    program_map = {}
    for item in iterable_of_objects_to_explore:
        if item[0] not in set_to_block_repeats:
            set_to_block_repeats.add(item[0])
            if inspect.isfunction(item[1]):
                program_map[item[0]] = item[0] + ' function'
            elif inspect.isclass(item[1]) or inspect.ismodule(item[1]):
                suffix = ' class' if inspect.isclass(item[1]) else ' module'
                temporary_output = recusively_construct_dict_of_all_objects_from_object(
                    inspect.getmembers(item[1]), recursion_floor - 1, set_to_block_repeats)
                for member in temporary_output:
                    program_map[item[0] + '.' +
                                member] = temporary_output[member] + suffix
            else:
                program_map[item[0]] = item[0] + \
                    get_string_of_class_from_object(item[1])
    return program_map


def search_dict_of_everything_for_sentence(everything, sentence, number, nlp):
    sentence_vector = nlp(sentence)[0]
    distances_from_vectors = []
    for key in everything:
        distances_from_vectors.append([calc_dist(sentence_vector, everything[key]['embedding_representation']), key]
                                      )
    distances_from_vectors.sort()
    return distances_from_vectors[:number]


def display_semantic_candidates(dict_of_everything, candidates):
    if len(candidates) == 0:
        print("There were no candidates!")
        exit()
    print("\nSimilar semantic candidates include:")
    for item in candidates:
        print(item[1] + ' : ' + dict_of_everything[item[1]]
              ['sentence_representation'])


def run_semantic_search_through_program():
    try:
        nlp = load_model()
    except Exception as e:
        print(e)
        "Likely a dependencies error. Try running: `pip3 install --upgrade tensorflow-text tensorflow-hub inspect`"
        exit()
    module = input("What module would you like to explore?\n")
    dict_of_everything = recusively_construct_dict_of_all_objects_from_object(
        __import__(module))
    for key in dict_of_everything:
        sentence_representation = parse_text_into_sentence_for_vectorization(
            dict_of_everything[key])
        dict_of_everything[key] = {
            'sentence_representation': sentence_representation,
            'embedding_representation': nlp(sentence_representation)[0]
        }
    while True:
        answer = input(
            "\nWhat function in the library are you interesting in exploring?\n")
        number = input(
            "\nHow many objects would you like in your result? (integer answers only)\n")
        try:
            number = int(number)
        except:
            print("That wasn't a number. Never mind, then")
            exit()
        candidates_list = search_dict_of_everything_for_sentence(
            dict_of_everything, answer, number, nlp)
        display_semantic_candidates(dict_of_everything, candidates_list)


if __name__ == "__main__":
    run_semantic_search_through_program()
