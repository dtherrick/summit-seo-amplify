2025-05-16T19:27:54.051Z [INFO]: # Cloning repository: git@github.com:dtherrick/summit-seo-amplify.git
2025-05-16T19:27:54.911Z [INFO]: 
2025-05-16T19:27:54.911Z [INFO]: Cloning into 'summit-seo-amplify'...
2025-05-16T19:27:54.912Z [INFO]: # Switching to commit: c62081f8778beaf2efbf5f7ab3c6c7924a1bd7ee
2025-05-16T19:27:54.934Z [INFO]: Note: switching to 'c62081f8778beaf2efbf5f7ab3c6c7924a1bd7ee'.
                                 You are in 'detached HEAD' state. You can look around, make experimental
                                 changes and commit them, and you can discard any commits you make in this
                                 state without impacting any branches by switching back to a branch.
                                 If you want to create a new branch to retain commits you create, you may
                                 do so (now or later) by using -c with the switch command. Example:
                                 git switch -c <new-branch-name>
                                 Or undo this operation with:
                                 git switch -
                                 Turn off this advice by setting config variable advice.detachedHead to false
                                 HEAD is now at c62081f Refactor resource and app components for improved clarity and functionality
2025-05-16T19:27:54.986Z [INFO]: Successfully cleaned up Git credentials
2025-05-16T19:27:54.986Z [INFO]: # Checking for Git submodules at: /codebuild/output/src2806467430/src/summit-seo-amplify/.gitmodules
2025-05-16T19:27:54.993Z [INFO]: # Retrieving environment cache...
2025-05-16T19:27:55.035Z [WARNING]: ! Unable to write cache: {"code":"ERR_BAD_REQUEST","message":"Request failed with status code 404"})}
2025-05-16T19:27:55.035Z [INFO]: ---- Setting Up SSM Secrets ----
2025-05-16T19:27:55.035Z [INFO]: SSM params {"Path":"/amplify/d9e32iiq5ru07/connect-frontend-backend-user-apis/","WithDecryption":true}
2025-05-16T19:27:55.764Z [INFO]: # No package override configuration found.
2025-05-16T19:27:55.768Z [INFO]: # Retrieving cache...
2025-05-16T19:27:55.803Z [INFO]: # Retrieved cache
2025-05-16T19:28:00.132Z [INFO]: ## Starting Backend Build
                                 # Starting phase: build
                                 # Executing command: npm ci --cache .npm --prefer-offline
2025-05-16T19:28:14.977Z [WARNING]: npm error code EUSAGE
2025-05-16T19:28:14.984Z [WARNING]: npm error
                                    npm error The `npm ci` command can only install with an existing package-lock.json or
                                    npm error npm-shrinkwrap.json with lockfileVersion >= 1. Run an install with npm@5 or
                                    npm error later to generate a package-lock.json file, then try again.
                                    npm error
                                    npm error Clean install a project
                                    npm error
                                    npm error Usage:
                                    npm error npm ci
                                    npm error
                                    npm error Options:
                                    npm error [--install-strategy <hoisted|nested|shallow|linked>] [--legacy-bundling]
                                    npm error [--global-style] [--omit <dev|optional|peer> [--omit <dev|optional|peer> ...]]
                                    npm error [--include <prod|dev|optional|peer> [--include <prod|dev|optional|peer> ...]]
                                    npm error [--strict-peer-deps] [--foreground-scripts] [--ignore-scripts] [--no-audit]
                                    npm error [--no-bin-links] [--no-fund] [--dry-run]
                                    npm error [-w|--workspace <workspace-name> [-w|--workspace <workspace-name> ...]]
                                    npm error [-ws|--workspaces] [--include-workspace-root] [--install-links]
                                    npm error
                                    npm error aliases: clean-install, ic, install-clean, isntall-clean
                                    npm error
                                    npm error Run "npm help ci" for more info
                                    npm error A complete log of this run can be found in: /codebuild/output/src2806467430/src/summit-seo-amplify/.npm/_logs/2025-05-16T19_28_03_841Z-debug-0.log
2025-05-16T19:28:15.137Z [ERROR]: !!! Build failed
2025-05-16T19:28:15.138Z [ERROR]: !!! Error: Command failed with exit code 1
2025-05-16T19:28:15.138Z [INFO]: # Starting environment caching...
2025-05-16T19:28:15.138Z [INFO]: # Environment caching completed