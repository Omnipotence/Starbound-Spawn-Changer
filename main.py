import sys
import struct
from optparse import OptionParser

#   Starbound Spawn Coordinate Changer
#   Based on http://seancode.com/galileo/format/wrldb.html
#   usage: `python main.py -x coordinate -y coordinate worldfile'



KEY = bytearray([76, 76, 0, 0, 0, 1, 0, 0, 0, 0, 0])

WORLD_WIDTH_OFFSET = 0
WORLD_HEIGHT_OFFSET = 4
METADATA_LENGTH_OFFSET = 8

METADATA_VERSION_OFFSET = 0
METADATA_SPAWN_X_OFFSET = 4
METADATA_SPAWN_Y_OFFSET = 8

def main(argv):
    usage = "usage: %prog [options] world_file"
    parser = OptionParser(usage=usage)
    parser.add_option("-x",  action="store", type="float", dest="new_spawn_x", help="Change X coordinate of spawn", metavar="X_Coordinate")
    parser.add_option("-y",  action="store", type="float", dest="new_spawn_y", help="Change Y coordinate of spawn", metavar="Y_Coordinate")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        return 1



    filename_world = args[0]
    file = open(filename_world, "rb")
    world_bytes = bytearray(file.read())
    file.close()

    indices = find_key_indices(world_bytes)

    if len(indices) == 0:
        print "World header not found, unable to continue."
        return 1
    elif len(indices) > 1:
        print "Multiple matching world headers found, listing/updating all of them just to be sure."

    for index in indices:

        world_header_length = determine_length_of_packed_bytes(world_bytes, index + len(KEY))
        world_header_index = index + len(KEY) + world_header_length        
        width = get_int_from_bytes(world_bytes, world_header_index + WORLD_WIDTH_OFFSET)
        height = get_int_from_bytes(world_bytes, world_header_index + WORLD_HEIGHT_OFFSET)

        metadata_length = determine_length_of_packed_bytes(world_bytes, world_header_index + METADATA_LENGTH_OFFSET)
        metadata_header_index = world_header_index + METADATA_LENGTH_OFFSET + metadata_length
        version = get_int_from_bytes(world_bytes, metadata_header_index + METADATA_VERSION_OFFSET)
        spawn_x = get_float_from_bytes(world_bytes, metadata_header_index + METADATA_SPAWN_X_OFFSET)
        spawn_y = get_float_from_bytes(world_bytes, metadata_header_index + METADATA_SPAWN_Y_OFFSET)
        
        if options.new_spawn_x == None and options.new_spawn_y == None:
            print ""
            print "World header at index %d" % world_header_index
            print "Width: %d" % width
            print "Height: %d" % height
            print "Version: %d" % version
            print "Spawn X: %s" % str(spawn_x)
            print "Spawn Y: %s" % str(spawn_y)

        else:
            if options.new_spawn_x != None:
                new_spawn_x_bytes = struct.pack('!f', options.new_spawn_x)
                for i in range(0, 4):
                    world_bytes[metadata_header_index + METADATA_SPAWN_X_OFFSET + i] = new_spawn_x_bytes[i]
                print "Spawn X set to: %s" %str(get_float_from_bytes(world_bytes, metadata_header_index + METADATA_SPAWN_X_OFFSET))

            if options.new_spawn_y != None:
                new_spawn_y_bytes = struct.pack('!f', options.new_spawn_y)
                for i in range(0, 4):
                    world_bytes[metadata_header_index + METADATA_SPAWN_Y_OFFSET + i] = new_spawn_y_bytes[i]
                print "Spawn Y set to: %s" %str(get_float_from_bytes(world_bytes, metadata_header_index + METADATA_SPAWN_Y_OFFSET))
            
            file = open(filename_world, "wb")
            file.write(world_bytes)
            file.close

    # Done
    return 0


def find_key_indices(world_bytes):
    index = 0
    indices = []
    while(index != -1):
        index = world_bytes.find(KEY, index + 1)
        if(index != -1):
            indices.append(index)
    return indices

def determine_length_of_packed_bytes(world_bytes, index):
    length = 1
    done = False
    current_index = index
    while (not done):
        if (world_bytes[current_index] >= 128):
            length = length + 1
            current_index = current_index + 1
        else:
            done = True
    return length

def get_int_from_bytes(world_bytes, index):
    return (256**3 * world_bytes[index]) + (256**2 * world_bytes[index + 1]) + (256 * world_bytes[index + 2]) + world_bytes[index + 3] 

def get_float_from_bytes(world_bytes, index):
    return struct.unpack('!f', str(world_bytes[index : index + 4]))

if __name__ == "__main__":
    sys.exit(main(sys.argv))