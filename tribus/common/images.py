import cairo
import rsvg

def svg2png(input_file=None, output_file=None):
	assert input_file is not None
	assert output_file is not None

	svg = rsvg.Handle(file=input_file)
	width = svg.props.width
	height = svg.props.height

	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
	context = cairo.Context(surface)

	try:
		svg.render_cairo(context)
		surface.write_to_png(output_file)
	except Exception, e:
		raise e
	else:
		return True
