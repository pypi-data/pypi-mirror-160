from biolib.biolib_binary_format.base_bbf_package import BioLibBinaryFormatBasePackage
from biolib.biolib_binary_format.utils import IndexableBuffer


class ModuleInput(BioLibBinaryFormatBasePackage):
    def __init__(self, bbf=None):
        super().__init__(bbf)
        self.package_type = 1

    def serialize(self, stdin, arguments, files) -> bytes:
        bbf_data = bytearray()
        bbf_data.extend(self.version.to_bytes(1, 'big'))
        bbf_data.extend(self.package_type.to_bytes(1, 'big'))

        bbf_data.extend(len(stdin).to_bytes(8, 'big'))

        argument_len = sum([len(arg.encode()) for arg in arguments]) + (2 * len(arguments))
        bbf_data.extend(argument_len.to_bytes(4, 'big'))

        file_data_len = sum([len(data) + len(path.encode()) for path, data in files.items()]) + (12 * len(files))
        bbf_data.extend(file_data_len.to_bytes(8, 'big'))

        bbf_data.extend(stdin)

        for argument in arguments:
            encoded_argument = argument.encode()
            bbf_data.extend(len(encoded_argument).to_bytes(2, 'big'))
            bbf_data.extend(encoded_argument)

        for path, data in files.items():
            encoded_path = path.encode()
            bbf_data.extend(len(encoded_path).to_bytes(4, 'big'))
            bbf_data.extend(len(data).to_bytes(8, 'big'))

            bbf_data.extend(encoded_path)
            bbf_data.extend(data)

        return bbf_data

    def deserialize(self):
        version = self.get_data(1, output_type='int')
        package_type = self.get_data(1, output_type='int')
        self.check_version_and_type(version=version, package_type=package_type, expected_package_type=self.package_type)

        stdin_len = self.get_data(8, output_type='int')
        argument_data_len = self.get_data(4, output_type='int')
        files_data_len = self.get_data(8, output_type='int')
        stdin = self.get_data(stdin_len)

        end_of_arguments = self.pointer + argument_data_len
        arguments = []
        while self.pointer != end_of_arguments:
            argument_len = self.get_data(2, output_type='int')
            argument = self.get_data(argument_len, output_type='str')
            arguments.append(argument)

        end_of_files = self.pointer + files_data_len
        files = {}
        while self.pointer < end_of_files:
            path_len = self.get_data(4, output_type='int')
            data_len = self.get_data(8, output_type='int')
            path = self.get_data(path_len, output_type='str')
            data = self.get_data(data_len)
            files[path] = bytes(data)

        return {'stdin': stdin, 'arguments': arguments, 'files': files}

    def convert_to_serialized_module_input(self, buffer: IndexableBuffer) -> bytes:
        # Don't need version and package type
        version = buffer.get_data_with_pointer_as_int(1)
        package_type = buffer.get_data_with_pointer_as_int(1)

        self.check_version_and_type(version=version, package_type=package_type, expected_package_type=self.package_type)

        stdin_len = buffer.get_data_with_pointer_as_int(8)
        argument_data_len = buffer.get_data_with_pointer_as_int(4)
        files_data_len = buffer.get_data_with_pointer_as_int(8)
        stdin = buffer.get_data_with_pointer(stdin_len)

        end_of_arguments = buffer.pointer + argument_data_len
        arguments = []
        while buffer.pointer != end_of_arguments:
            argument_len = buffer.get_data_with_pointer_as_int(2)
            argument = buffer.get_data_with_pointer_as_string(argument_len)
            arguments.append(argument)

        end_of_files = buffer.pointer + files_data_len
        files = {}
        while buffer.pointer < end_of_files:
            path_len = buffer.get_data_with_pointer_as_int(4)
            data_len = buffer.get_data_with_pointer_as_int(8)
            path = buffer.get_data_with_pointer_as_string(path_len)
            data = buffer.get_data_with_pointer(data_len)
            files[path] = bytes(data)

        return ModuleInput().serialize(
            arguments=arguments,
            files=files,
            stdin=stdin
        )
