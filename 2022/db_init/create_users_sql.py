import sys
import os

out = ""
skel = "INSERT INTO Names (surname, famname) VALUES ('{SURNAME}', '{FAMNAME}');\n"
out_path = "_names.sql"

if len(sys.argv) < 3:
    print("usage: create_users_sql.py <init/drop> members.csv [opt: <path/to/output.sql>]")
else:
    if not ("init" in sys.argv[1]):
        out += "DROP TABLE Names;"
    out += """
    CREATE TABLE Names (
      id         INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
      surname    VARCHAR(255) NOT NULL,
      famname    VARCHAR(255) NOT NULL
    );

    """
    if len(sys.argv) > 3:
        if not sys.argv[3].endswith(".sql"):
            out_path = f"{sys.argv[3]}.sql"
        else:
            out_path = sys.argv[3]

    try:
        with open(sys.argv[2], 'r') as f:
            for l in f.readlines():
                out += skel.format(SURNAME=l.strip().split()[0], FAMNAME=l.strip().split()[1])
                #out += skel.format(NAME=" ".join(l.strip().split()))

            with open(out_path, 'w') as f:
                f.write(out)
    except FileNotFoundError:
        print(f"{sys.argv[2]} not found.")
