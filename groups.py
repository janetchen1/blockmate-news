import pprint
import sheet_utils


def MakeGroupDict(g_sheet, u_sheet):
	"""
	Creates a directory with following structure:

	group ids: {
					submission spreadsheet name,
					submitter directory: {
						group member name: {
							email
							submission count
						}
					}
	}
	"""
	groups_sheet = sheet_utils.GetSheet(g_sheet)
	group_list = sheet_utils.GetRows(groups_sheet)

	group_directory = {}
	for group in group_list:
		gid = group['group_id']
		group_directory[gid] = {}
		group_directory[gid]['sp_name'] = group['spreadsheet_name']
		group_directory[gid]['submission_form'] = group['submission_form']
		group_directory[gid]['admin_email'] = group['admin']
		group_directory[gid]['submitter_directory'] = {}
		name_list = group['name_list'].split(', ')
		for name in name_list:
			group_directory[gid]['submitter_directory'][name] = {}
			group_directory[gid]['submitter_directory'][name]['count'] = 0

	# fill in user emails using u_sheet
	users_sheet = sheet_utils.GetSheet(u_sheet)
	user_list = sheet_utils.GetRows(users_sheet)

	for user in user_list:
		user_group = user['group_id']
		email = user['email']
		name = user['name']
		group_directory[user_group]['submitter_directory'][name]['email'] = email

	return group_directory
