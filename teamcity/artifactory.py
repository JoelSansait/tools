__copyright__ = 'Anki Inc. 2014'
__author__ = 'ben@anki.com'

# Modifications made by jsansait@nvidia.com

import os
import sys
import json
import base64
import argparse
import requests

def list_projects():
    url = "/httpAuth/app/rest/projects"
    projects = query_tc_api(url)
    ret = []
    for p in projects['project']:
        ret.append(p['id'])

    return json.dumps({'projects': ret}, sort_keys=True, indent=4, separators=(',', ': '))

def list_subprojects(project):
    url = "/httpAuth/app/rest/projects/id:%s" % project
    try:
        subprojects = query_tc_api(url)['projects']['project']
    except KeyError:
        print >>sys.stderr, "That project has no subprojects."
        sys.exit(1)

    ret = []
    for p in subprojects:
        ret.append(p['id'].split('_')[1])
    return json.dumps({'project': project, 'subprojects': ret}, sort_keys=True, indent=4, separators=(',', ': '))

def list_build_types(project, sub):
    url = "/httpAuth/app/rest/projects/id:%s" % "_".join([project, sub])
    build_types = query_tc_api(url)['buildTypes']['buildType']

    ret = [b['id'] for b in build_types]
    return json.dumps({'project': project, 'subprojects': sub, 'build_types': ret}, sort_keys=True, indent=4, separators=(',', ': '))

def list_tags(project, sub, bt):
    url = "/httpAuth/app/rest/builds/?locator=buildType:%s,lookupLimit:10" % bt
    builds = query_tc_api(url)['build']
    build_hrefs = [b['href'] for b in builds]
    ret = []
    for h in build_hrefs:
        tags = query_tc_api(h)['tags']
        for t in tags['tag']:
            if len(t) == 40:
                ret.append(t)
    return json.dumps({
        'project': project,
        'subproject': sub,
        'build_type': bt,
        'tags': ret},
        sort_keys=True, indent=4, separators=(',', ': '))

def list_artifacts(project, sub, bt, tag):
    build_id = get_build_id(bt, tag)

    url = "/httpAuth/app/rest/builds/id:%s/artifacts" % build_id
    artifacts = query_tc_api(url)['files']
    ret = [a['name'] for a in artifacts]
    return json.dumps({'project': project, 'subproject': sub, 'build_type': bt, 'tag': tag, 'artifacts': ret}, sort_keys=True, indent=4, separators=(',', ': '))

def get_artifact(project, sub, bt, tag, artifact):
    build_id = get_build_id(bt, tag)
    url = "/httpAuth/app/rest/builds/id:%s/artifacts/content/%s" % (build_id, artifact)
    print "Downloading artifact to %s" % artifact
    print "Or get it yourself: "
    creds = base64.b64encode("{0}:{1}".format(username, password))
    print "\tcurl -o {0} -H 'Authorization: {1}' {2}{3}".format(artifact, creds, host, url)
    r = requests.get(host, auth=(username, password))
    output = open(artifact, "w")
    output.write(r.content)
    output.close()
    sys.exit(0)

def get_build_id(bt, tag):
    url = "/httpAuth/app/rest/builds/?locator=buildType:%s,tags:%s,status:SUCCESS" % (bt, tag)
    builds = query_tc_api(url)['build']
    build = sorted(builds, key=lambda k: k['number'], reverse=True)[0]
    return build['id']

def query_tc_api(url):
    teamcity = host + url
    h = {"Accept": "Application/JSON"}
    r = requests.get(teamcity, auth=(username, password), headers=h)
    if r.status_code != 200:
        raise Exception("%s: %s" % (r.reason, r.text))
    return json.loads(r.text)

if __name__ == '__main__':
    username = os.getenv("TEAMCITY_USERNAME")
    password = os.getenv("TEAMCITY_PASSWORD")
    host = os.getenv("TEAMCITY_HOST")
    if not (username and password and host):
        print >>sys.stderr, "Must set TEAMCITY_USERNAME, TEAMCITY_PASSWORD, TEAMCITY_HOST env vars."
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', help='Name of TeamCity project')
    parser.add_argument('-s', '--subproject', help='Name of TeamCity subproject')
    parser.add_argument('-b', '--buildtype', help='Build type')
    parser.add_argument('-t', '--tag', help='Tag (usually the commit sha)')
    parser.add_argument('-a', '--artifact', help='Artifact to retrieve')

    args = vars(parser.parse_args())

    project = args.get('project')
    if not project:
        parser.print_help(sys.stderr)
        print >>sys.stderr, "\n\nMust supply project. Possible values: "
        print >>sys.stderr, list_projects()
        sys.exit(1)

    subproject = args.get('subproject')
    if not subproject:
        parser.print_help(sys.stderr)
        print >>sys.stderr, "\n\nMust supply subproject. Possible values: "
        print >>sys.stderr, list_subprojects(project)
        sys.exit(1)

    build_type = args.get('buildtype')
    if not build_type:
        parser.print_help(sys.stderr)
        print >>sys.stderr, "\n\nMust supply buildtype. Possible values: "
        print >>sys.stderr, list_build_types(project, subproject)
        sys.exit(1)

    tag = args.get('tag')
    if not tag:
        parser.print_help(sys.stderr)
        print >>sys.stderr, "\n\nMust supply tag. Possible values: "
        print >>sys.stderr, list_tags(project, subproject, build_type)
        sys.exit(1)

    artifact = args.get('artifact')
    if not artifact:
        parser.print_help(sys.stderr)
        print >>sys.stderr, "\n\nMust supply artifact. Possible values: "
        print >>sys.stderr, list_artifacts(project, subproject, build_type, tag)
        sys.exit(1)

    get_artifact(project, subproject, build_type, tag, artifact)

