from beets.plugins import BeetsPlugin
from beets.ui import Subcommand
from beets import library

def mbhelper(lib, opts, args):
        # SQL Queries
        with lib.transaction() as tx:
            sharedacoustids = tx.query("""SELECT acoustid_id, album, mb_albumid, albumartist, mb_artistid, title, artist, mb_trackid
                                            FROM items
                                           WHERE acoustid_id IN (SELECT acoustid_id 
                                                                   FROM items
                                                                   WHERE acoustid_id != ''
                                                                   GROUP BY acoustid_id
                                                                  HAVING count(distinct mb_trackid)  > 1)
                                                                   ORDER BY acoustid_id, mb_trackid;""")
                        
            multipleacoustids = tx.query("""SELECT acoustid_id, album, mb_albumid, albumartist, mb_artistid, title, artist, mb_trackid
                                              FROM items
                                             WHERE mb_trackid IN (SELECT mb_trackid 
                                                                    FROM items
                                                                   WHERE acoustid_id != ''
                                                                   GROUP BY mb_trackid
                                                                  HAVING count(distinct acoustid_id)  > 1)
                                                                   ORDER BY mb_trackid, acoustid_id;""")
        
        # HTML generation
        output = "<html><body>"
        output += '''<div class="topnav">
                        <h2>MusicBrainz Helper</h2>
                        <div id="categories">
                            <a href="javascript:void(0);" onclick="showSharedAcoustids()">Recordings With Shared Acoustids</a>
                            <a href="javascript:void(0);" onclick="showMultipleAcoustids()">Recordings With Multiple Acoustids</a>
                        </div>
                        <a href="javascript:void(0);" class="icon" onclick="showMenuContents()"><i class="fa fa-bars"></i></a>
                     </div><div id="content">'''
        
        # Recordings with shared Acoustids
        output += '''<div id="sharedacoustids"><div class="header"><h2>Recordings With Shared Acoustids</h2><p></div>
                     <div><p>This page lists tracks in your library that are linked to different MusicBrainz recordings but share the same acoustid. This may indicate that the recordings should be merged.
                     <br><br>
                     Shared acoustids are a good sign that recordings may need to be merged, but should not be the only thing you rely on. Acoustids group similar fingerprints and may sometimes group recordings that should remain separate in MusicBrainz (examples are clean vs explicit recordings, DJ mixes, or differences in intros or outros).<p></div>'''
        last_acoustid = ""
        for row in sharedacoustids:
            if last_acoustid == "":
                output += "<div class=\"accordion\"><strong>Acoustid <a href=\"https://acoustid.org/track/" + row["acoustid_id"] + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + row["acoustid_id"] + "</a></strong></div><div class=\"recordings\"><table><tr><th>Recording Title</th><th>Recording Artist</th><th>Release Title</th><th>Release Artist</th></tr>"
                last_acoustid = row["acoustid_id"]
            elif last_acoustid != row["acoustid_id"]:
                output += "</table></div><br><div class=\"accordion\"><strong>Acoustid <a href=\"https://acoustid.org/track/" + row["acoustid_id"] + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + row["acoustid_id"] + "</a></strong></div><div class=\"recordings\"><table><tr><th>Recording Title</th><th>Recording Artist</th><th>Release Title</th><th>Release Artist</th></tr>"
                last_acoustid = row["acoustid_id"]
            output += "<tr><td><a href=\"https://musicbrainz.org/recording/" + row["mb_trackid"] + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + row["title"] + "</td><td>" + row["artist"] + "</td><td><a href=\"https://musicbrainz.org/release/" + row["mb_albumid"] + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + row["album"] + "</a></td><td>" + row["albumartist"] + "</td></tr>"
        output += "</table></div></div>"

        # Recordings with multiple Acoustids
        output += '''<div id="multipleacoustids"><div class="header"><h2>Recordings With Multiple Acoustids</h2><p>
                     <div><p>This page lists tracks in your library that share MusicBrainz recordings but do not have matching acoustids. This may indicate a mistaken recording merge in the past that needs to be split.
                     <br><br>
                     <strong>This list has a very high false positive rate.</strong> Differences in the speed of a recording, added noise (such as from a vinyl rip), or other small differences between releases can cause the same recording to have multiple acoustids. Please review the acoustids individually on acoustid.org (the fingerprint comparison tool is good for this purpose) and use common sense before splitting a recording.<p>'''
        last_recordingid = ""
        for row in multipleacoustids:
            if last_recordingid == "":
                output += "<div class=\"accordion\"><strong>Recording ID <a href=\"https://musicbrainz.org/recording/" + row["mb_trackid"] + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + row["mb_trackid"] + "</a></strong></div><div class=\"recordings\"><table><tr><th>Recording Title</th><th>Recording Artist</th><th>Acoustid</th><th>Release Title</th><th>Release Artist</th></tr>"
                last_recordingid = row["mb_trackid"]
            if last_recordingid != row["mb_trackid"]:
                output += "</table></div><br><div class=\"accordion\"><strong>Recording ID <a href=\"https://musicbrainz.org/recording/" + row["mb_trackid"] + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + row["mb_trackid"] + "</a></strong></div><div class=\"recordings\"><table><tr><th>Recording Title</th><th>Recording Artist</th><th>Acoustid</th><th>Release Title</th><th>Release Artist</th></tr>"
                last_recordingid = row["mb_trackid"]
            output += "<tr><td><a href=\"https://musicbrainz.org/recording/" + row["mb_trackid"] + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + row["title"] + "</td><td>" + row["artist"] + "</td><td><a href=\"https://acoustid.org/track/" + row["acoustid_id"] + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + row["acoustid_id"] + "</a></td><td><a href=\"https://musicbrainz.org/release/" + row["mb_albumid"] + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + row["album"] + "</a></td><td>" + row["albumartist"] + "</td></tr>"

        # HTML Generation
        output += "</table></div></div></div></body></html>"

        # JavaScript
        output += '''<script>
                        var acc = document.getElementsByClassName("accordion");
                        var i;
                        for (i = 0; i < acc.length; i++) {
                            acc[i].addEventListener("click", function() {
                                this.classList.toggle("active");
                                var panel = this.nextElementSibling;
                                if (panel.style.display === "block") {
                                    panel.style.display = "none";
                                } else {
                                    panel.style.display = "block";
                                }
                            });
                        }

                        function showMenuContents() {
                            var x = document.getElementById("categories");
                            if (x.style.display === "block") {
                                x.style.display = "none";
                            } else {
                                x.style.display = "block";
                            }
                        }

                        function showSharedAcoustids() {
                            document.getElementById("sharedacoustids").style.display = "inline";
                            document.getElementById("multipleacoustids").style.display = "none";
                        }

                        function showMultipleAcoustids() {
                            document.getElementById("multipleacoustids").style.display = "inline";
                            document.getElementById("sharedacoustids").style.display = "none";
                        }
                    </script>'''
        # CSS
        output += '''   
                        <link rel="preconnect" href="https://fonts.googleapis.com">
                        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
                        <style>
                            .accordion {
                                background-color: #FFF;
                                color: #444;
                                cursor: pointer;
                                padding: 18px;
                                width: 100%;
                                border: none;
                                border-top: solid 1px #999;
                                border-bottom: solid 1px #999;
                                border-left: solid 1px #CCC;
                                border-right: 1px solid #999;
                                text-align: left;
                                outline: none;
                                font-size: 15px;
                                transition: 0.4s;
                            }

                            .accordion:hover {
                                background-color: #ccc; 
                            }

                            .recordings {
                                padding: 0 18px;
                                display: none;
                                background-color: white;
                                overflow: hidden;
                                color: #666;
                            }

                            body {
                                font-family: "Noto Sans", sans-serif;
                                font-size: 12px;
                                font-variation-settings:
                                    "wdth" 100;
                            }

                            p {
                                font-size: 16px;
                            }

                            .topnav {
                                position: sticky;
                                top: 0;
                                width: 100%;
                                border-bottom: #BA478F 2px solid;
                                z-index: 1;
                                background-color: white;
                            }

                            .topnav #categories {
                                display: none;
                            }

                            .topnav a {
                                color: #BA478F;
                                padding: 14px 16px;
                                text-decoration: none;
                                font-size: 17px;
                                display: block;
                            }

                            #multipleacoustids {
                                display: none;
                            }

                            .topnav a.icon {
                                display: block;
                                position: absolute;
                                right: 0;
                                top: 5px;
                                color: #BA478F;
                                padding: 0px 16px;
                            }
                                
                            a {
                                color: #002BBA;
                                text-decoration: none;
                            }

                            table {
                                border-collapse: collapse;
                            }

                            td, th {
                                border: 1px solid #dddddd;
                                text-align: left;
                                padding: 8px;
                            }

                            tr:nth-child(even) {
                                background-color: #dddddd;
                            }'''
        
        # Write HTML to file and save
        fileName = "Beets-MusicBrainz Helper Report.html"
        if opts.directory is None:
            directory = fileName
        else:
            directory = opts.directory.removesuffix("/") + "/" + fileName

        Html_file=open(directory ,"w")
        Html_file.write(output)
        Html_file.close()

        print("Your report has been generated and saved in the given directory with the name \""+ fileName +"\"")

class MBHelperPlugin(BeetsPlugin):
    def commands(self):
        mbhelper_cmd = Subcommand('mbhelper', help='generate a report of your library for use with MusicBrainz')
        mbhelper_cmd.parser.add_option(
            "-d",
            "--directory",
            dest="directory",
            help="directory to place musicbrainz report in"
        )
        mbhelper_cmd.func = mbhelper
        return [mbhelper_cmd]