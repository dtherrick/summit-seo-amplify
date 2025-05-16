0

2025-05-16T20:10:40.920Z [INFO]: # Cloning repository: git@github.com:dtherrick/summit-seo-amplify.git

1

2025-05-16T20:10:41.683Z [INFO]: 

2

2025-05-16T20:10:41.684Z [INFO]: Cloning into 'summit-seo-amplify'...

3

2025-05-16T20:10:41.684Z [INFO]: # Switching to commit: f5d9614511ac98c9b2dc09b7effc028b28bb3da1

4

2025-05-16T20:10:41.708Z [INFO]: Note: switching to 'f5d9614511ac98c9b2dc09b7effc028b28bb3da1'.

5

                                 You are in 'detached HEAD' state. You can look around, make experimental

6

                                 changes and commit them, and you can discard any commits you make in this

7

                                 state without impacting any branches by switching back to a branch.

8

                                 If you want to create a new branch to retain commits you create, you may

9

                                 do so (now or later) by using -c with the switch command. Example:

10

                                 git switch -c <new-branch-name>

11

                                 Or undo this operation with:

12

                                 git switch -

13

                                 Turn off this advice by setting config variable advice.detachedHead to false

14

                                 HEAD is now at f5d9614 Comment out backend build phase in amplify.yml to resolve npm ci issues during Amplify build process

15

2025-05-16T20:10:41.761Z [INFO]: Successfully cleaned up Git credentials

16

2025-05-16T20:10:41.761Z [INFO]: # Checking for Git submodules at: /codebuild/output/src3050365332/src/summit-seo-amplify/.gitmodules

17

2025-05-16T20:10:41.767Z [INFO]: # Retrieving environment cache...

18

2025-05-16T20:10:41.796Z [WARNING]: ! Unable to write cache: {"code":"ERR_BAD_REQUEST","message":"Request failed with status code 404"})}

19

2025-05-16T20:10:41.796Z [INFO]: ---- Setting Up SSM Secrets ----

20

2025-05-16T20:10:41.796Z [INFO]: SSM params {"Path":"/amplify/d9e32iiq5ru07/connect-frontend-backend-user-apis/","WithDecryption":true}

21

2025-05-16T20:10:42.515Z [INFO]: # No package override configuration found.

22

2025-05-16T20:10:42.519Z [INFO]: # Retrieving cache...

23

2025-05-16T20:10:42.570Z [INFO]: # Retrieved cache

24

2025-05-16T20:10:43.813Z [INFO]: BackendEnvironment name connect-frontend-backend-user-apis for app d9e32iiq5ru07 is invalid

25

2025-05-16T20:10:43.891Z [INFO]: Random environment name sarena generated

26

2025-05-16T20:10:46.345Z [INFO]: ## Starting Backend Build

27

                                 ## Checking for associated backend environment...

28

                                 ## No backend environment association found, continuing...

29

                                 ## Completed Backend Build

30

2025-05-16T20:10:46.351Z [INFO]: {"backendDuration": 0}

31

                                 ## Starting Frontend Build

32

                                 # Starting phase: build

33

                                 # Executing command: cd frontend

34

2025-05-16T20:10:46.386Z [INFO]: # Executing command: npm ci

35

2025-05-16T20:11:06.280Z [WARNING]: npm warn ERESOLVE overriding peer dependency

36

2025-05-16T20:11:06.288Z [WARNING]: npm warn While resolving: @xstate/react@3.2.2

37

                                    npm warn Found: react@19.1.0

38

                                    npm warn node_modules/react

39

                                    npm warn   react@"^19.1.0" from the root project
100

                                    npm warn EBADENGINE   required: { node: '20 || >=22' },

101

                                    npm warn EBADENGINE   current: { node: 'v18.20.8', npm: '10.8.2' }

102

                                    npm warn EBADENGINE }

103

2025-05-16T20:11:06.356Z [WARNING]: npm warn EBADENGINE Unsupported engine {

104

                                    npm warn EBADENGINE   package: 'jackspeak@4.1.0',

105

                                    npm warn EBADENGINE   required: { node: '20 || >=22' },

106

                                    npm warn EBADENGINE   current: { node: 'v18.20.8', npm: '10.8.2' }

107

                                    npm warn EBADENGINE }

108

2025-05-16T20:11:06.356Z [WARNING]: npm warn EBADENGINE Unsupported engine {

109

                                    npm warn EBADENGINE   package: 'lru-cache@11.1.0',

110

                                    npm warn EBADENGINE   required: { node: '20 || >=22' },

111

                                    npm warn EBADENGINE   current: { node: 'v18.20.8', npm: '10.8.2' }

112

                                    npm warn EBADENGINE }

113

2025-05-16T20:11:06.356Z [WARNING]: npm warn EBADENGINE Unsupported engine {

114

                                    npm warn EBADENGINE   package: 'minimatch@10.0.1',

115

                                    npm warn EBADENGINE   required: { node: '20 || >=22' },

116

                                    npm warn EBADENGINE   current: { node: 'v18.20.8', npm: '10.8.2' }

117

                                    npm warn EBADENGINE }

118

2025-05-16T20:11:06.356Z [WARNING]: npm warn EBADENGINE Unsupported engine {

119

                                    npm warn EBADENGINE   package: 'path-scurry@2.0.0',

120

                                    npm warn EBADENGINE   required: { node: '20 || >=22' },

121

                                    npm warn EBADENGINE   current: { node: 'v18.20.8', npm: '10.8.2' }

122

                                    npm warn EBADENGINE }

123

2025-05-16T20:11:06.357Z [WARNING]: npm warn EBADENGINE Unsupported engine {

124

                                    npm warn EBADENGINE   package: 'glob@11.0.2',

125

                                    npm warn EBADENGINE   required: { node: '20 || >=22' },

126

                                    npm warn EBADENGINE   current: { node: 'v18.20.8', npm: '10.8.2' }

127

                                    npm warn EBADENGINE }


140

                                    npm warn EBADENGINE   required: { node: '20 || >=22' },

141

                                    npm warn EBADENGINE   current: { node: 'v18.20.8', npm: '10.8.2' }

142

                                    npm warn EBADENGINE }

143

2025-05-16T20:11:06.357Z [WARNING]: npm warn EBADENGINE Unsupported engine {

144

                                    npm warn EBADENGINE   package: 'path-scurry@2.0.0',

145

                                    npm warn EBADENGINE   required: { node: '20 || >=22' },

146

                                    npm warn EBADENGINE   current: { node: 'v18.20.8', npm: '10.8.2' }

147

                                    npm warn EBADENGINE }

148

2025-05-16T20:11:06.371Z [WARNING]: npm error code EUSAGE

149

2025-05-16T20:11:06.371Z [WARNING]: npm error

150

                                    npm error `npm ci` can only install packages when your package.json and package-lock.json or npm-shrinkwrap.json are in sync. Please update your lock file with `npm install` before continuing.

151

                                    npm error

152

                                    npm error Missing: json-schema-to-ts@3.1.1 from lock file

153

                                    npm error Missing: @babel/runtime@7.27.1 from lock file

154

                                    npm error Missing: ts-algebra@2.0.0 from lock file

155

                                    npm error

156

                                    npm error Clean install a project

157

                                    npm error

158

                                    npm error Usage:

159

                                    npm error npm ci

160

                                    npm error

161

                                    npm error Options:

162

                                    npm error [--install-strategy <hoisted|nested|shallow|linked>] [--legacy-bundling]

163

                                    npm error [--global-style] [--omit <dev|optional|peer> [--omit <dev|optional|peer> ...]]

164

                                    npm error [--include <prod|dev|optional|peer> [--include <prod|dev|optional|peer> ...]]

165

                                    npm error [--strict-peer-deps] [--foreground-scripts] [--ignore-scripts] [--no-audit]

166

                                    npm error [--no-bin-links] [--no-fund] [--dry-run]

167

                                    npm error [-w|--workspace <workspace-name> [-w|--workspace <workspace-name> ...]]

168

                                    npm error [-ws|--workspaces] [--include-workspace-root] [--install-links]

169

                                    npm error

170

                                    npm error aliases: clean-install, ic, install-clean, isntall-clean

171

                                    npm error

172

                                    npm error Run "npm help ci" for more info

173

2025-05-16T20:11:06.372Z [WARNING]: npm error A complete log of this run can be found in: /root/.npm/_logs/2025-05-16T20_10_49_338Z-debug-0.log

174

2025-05-16T20:11:06.416Z [ERROR]: !!! Build failed

175

2025-05-16T20:11:06.416Z [ERROR]: !!! Error: Command failed with exit code 1

176

2025-05-16T20:11:06.417Z [INFO]: # Starting environment caching...

177

2025-05-16T20:11:06.417Z [INFO]: # Environment caching completed

178

179

