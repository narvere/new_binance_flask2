with op.batch_alter_table('posts') as batch_op:
    batch_op.drop_column('tags')