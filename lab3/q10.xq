(:10. Group the movies by genre and sort them by user rating within each genre.:)

let $nl := "&#10;"
let $videos := doc("videos.xml")/result/videos/video

let $output :=
    for $outergenre in distinct-values($videos/genre)
    let $videoswithoutergenre := concat('    <title>', string-join(
            for $video in $videos
            order by $video/user_rating descending
            return $video[genre = $outergenre]/title, '</title>&#10;    <title>'), "</title></genre>")
    return concat('<genre genre="', $outergenre, '">&#10;', $videoswithoutergenre)

return $output
