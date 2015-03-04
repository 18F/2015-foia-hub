
from django.db import connection
from django.db import migrations


def forwards(self, orm):
    sql = """
     CREATE FUNCTION agency_fts_document(integer) RETURNS tsvector AS $$
     DECLARE
         agency_document TEXT;
     BEGIN
         SELECT concat_ws(' ', name, description) INTO agency_document
         FROM foia_hub_agency WHERE id=$1;
         RETURN to_tsvector('pg_catalog.simple', agency_document);
     END;
     $$ LANGUAGE plpgsql;

     CREATE FUNCTION agency_fts_document_trigger() RETURNS TRIGGER AS $$
     BEGIN
         NEW.fts_document=agency_fts_document(NEW.id);
         RETURN NEW;
     END;
     $$ LANGUAGE plpgsql;
     """
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.execute(
        "ALTER TABLE foia_hub_agency ADD COLUMN fts_document tsvector;")
    cursor.execute(
        "UPDATE foia_hub_agency SET fts_document=agency_fts_document(id);")
    cursor.execute(
        """
        CREATE TRIGGER agency_fts_update_trigger BEFORE UPDATE ON
        foia_hub_agency FOR EACH ROW EXECUTE PROCEDURE
        agency_fts_document_trigger();
        """
    )
    cursor.execute(
        """
        CREATE TRIGGER agency_fts_insert_trigger BEFORE INSERT ON
        foia_hub_agency FOR EACH ROW EXECUTE PROCEDURE
        agency_fts_document_trigger();
        """
    )
    cursor.execute(
        """
        CREATE INDEX agency_fts_index ON foia_hub_agency USING
        gin(fts_document);
        """
    )


def backwards(self, orm):
    cursor = connection.cursor()
    cursor.execute("DROP INDEX agency_fts_index;")
    cursor.execute("ALTER TABLE foia_hub_agency DROP COLUMN fts_document;")
    cursor.execute(
        "DROP TRIGGER agency_fts_update_trigger ON foia_hub_agency;")
    cursor.execute(
        "DROP TRIGGER agency_fts_insert_trigger ON foia_hub_agency;")
    cursor.execute("DROP FUNCTION agency_fts_document (integer);")
    cursor.execute("DROP FUNCTION agency_fts_document_trigger ();")


class Migration(migrations.Migration):

    dependencies = [
        ('foia_hub', '0022_auto_20150301_2049'),
    ]

    operations = [
        migrations.RunPython(
            forwards,
            reverse_code=backwards
        )
    ]
