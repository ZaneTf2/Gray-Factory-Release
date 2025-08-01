import vtf2img_lib.parser as Parser
vtf_file = "Arena_lumberyard_event.vtf"
parser = Parser.Parser(vtf_file)
header = parser.header
print(f"\n\tVTF version: {header.version} \n\tImage Format: {header.image_format} \n\tImage size: {header.width}x{header.height}\n")
image = parser.get_image()

image.save("test.png")