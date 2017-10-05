(:3. Which are the top ten recommended movies? :)

let $videos := doc("videos.xml")/result/videos/video

let $topmovies :=
    for $video in $videos
    order by $video/user_rating descending
    return $video/title
return fn:subsequence($topmovies, 1, 10)
