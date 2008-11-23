def production():
    "Set the variables for the production environment"
    set(fab_hosts=["72.47.216.91"])
    set(fab_user="root")


def deploy(hash="HEAD"):
    "Deploy the application by packaging a specific hash or tag from the git repo"
    require("fab_hosts", provided_by=[production])
    require("fab_user", provided_by=[production])
    
    set(hash=hash)
    
    local("mkdir tmp")
    local("git archive -v --format=tar --prefix=deploy/ $(hash) conf build/libs build/taylanpince | gzip > tmp/archive.tar.gz")
    #local("rm -rf tmp")
