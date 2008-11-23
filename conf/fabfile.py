def production():
    "Set the variables for the production environment"
    set(fab_hosts=["72.47.216.91"])
    set(fab_user="root")
    set(remote_dir="/var/www/vhosts/taylanpince.com")


def deploy(hash="HEAD"):
    "Deploy the application by packaging a specific hash or tag from the git repo"
    # Make sure that the required variables are here
    require("fab_hosts", provided_by=[production])
    require("fab_user", provided_by=[production])
    require("remote_dir", provided_by=[production])
    
    # Set the commit hash (HEAD if not given)
    set(hash=hash)
    
    # Create a temporary local directory, export the given commit using git archive
    local("mkdir ../tmp")
    local("cd ..; git archive -v --format=tar --prefix=deploy/ $(hash) conf build/libs build/taylanpince | gzip > tmp/archive.tar.gz")
    
    # Upload the archive to the server
    put("../tmp/archive.tar.gz", "$(remote_dir)/archive.tar.gz")
    
    # Extract the files from the archive, remove the file
    run("cd $(remote_dir); tar -xzvf archive.tar.gz; rm -f archive.tar.gz")
    
    # Move directories out of the build folder and get rid of it
    run("mv $(remote_dir)/deploy/build/* $(remote_dir)/deploy/")
    run("rm -rf $(remote_dir)/deploy/build")
    
    # Create a symlink for the Django settings file
    run("ln -s $(remote_dir)/deploy/conf/settings.py $(remote_dir)/deploy/taylanpince/settings_local.py")
    
    # Move the uploaded files directory from the active version to the new version, create a symlink
    run("mv $(remote_dir)/app/files $(remote_dir)/deploy/files")
    run("ln -s $(remote_dir)/deploy/files $(remote_dir)/deploy/taylanpince/media/files")
    
    # Remove the active version of the app and move the new one in its place
    run("rm -rf $(remote_dir)/app")
    run("mv $(remote_dir)/deploy $(remote_dir)/app")
    
    # Restart Apache
    run("/usr/sbin/apachectl graceful")
    
    # Remove the temporary local directory
    local("rm -rf ../tmp")
