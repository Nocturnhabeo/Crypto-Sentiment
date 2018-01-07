
from google.cloud import bigtable

instance_id = ''
project_id = ''

client = bigtable.Client(project=project_id, admin=True)
instance = client.instance(instance_id)



if __name__ == '__main__':
	table = instance.table(table_id)
	table.create()
	column_family_id = 'twitter_farm'
	twitter_farm = table.column_family(column_family_id)
	twitter_farm.create()