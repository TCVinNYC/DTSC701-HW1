def compress_message(msg):
    if not msg:
        return "Please enter a message"

    compressed_msg = ""
    previous_character = ''
    temp_count = 1 

    # Iterate over the string
    for character in msg:
        if character == previous_character:
            temp_count += 1
        else:
            print(f'different character {character}')
            if temp_count > 1 :
                    compressed_msg += f"{previous_character}{temp_count}"
                    print(f'added old character to msg with compression {previous_character}{temp_count}')
            else:
                 compressed_msg += previous_character
                 print(f'added old character to msg without compression {previous_character}')
            previous_character = character
            temp_count = 1

    ## dumb fix to get the very last character checked and added to the final string
    if temp_count > 1 :
        compressed_msg += f"{previous_character}{temp_count}"
        print(f'added old character to msg with compression {previous_character}{temp_count}')
    else:
        compressed_msg += previous_character
        print(f'added old character to msg without compression {previous_character}')
    return compressed_msg

# Test cases
print(f" FINAL COMPRESSION - {compress_message('abcaaabbb')}")
print(f" FINAL COMPRESSION - {compress_message('abcd')}")