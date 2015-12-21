from lib import constants

def append_vdd_slide(vdd, slide):
		'''
			Picovico: Appends image slides into the project with data
		'''
		if vdd:
			if not vdd['assets']:
				vdd['assets'] = []

			last_slide = None
			current_slides_count = len(vdd['assets'])
			last_end_time = 0

			if vdd['assets']:
				last_slide = vdd['assets'][len(vdd['assets']) - 1]

				if last_slide:
					last_end_time = last_slide["end_time"]
				else:
					last_end_time = last_slide.end_time

			slide['start_time'] = last_end_time
			slide['end_time'] = last_end_time + constants.STANDARD_SLIDE_DURATION

			vdd['assets'].append(slide)
			return vdd

def append_music(vdd):
		'''
			Picovico: If music is set and not appended to the VDD slide, appends the music as vdd slide
		'''
		if vdd['_music']:
			append_vdd_slide(vdd, vdd['_music'])
			del vdd['_music']

def reset_slides(vdd):
		vdd['assets'] = []

def reset_music(vdd):
	del vdd['_music']
