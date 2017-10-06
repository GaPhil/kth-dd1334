(:9. Which movie should you recommend to a customer if they want to see a horror movie and do not have a laserdisk?:)

let $videos := doc("videos.xml")/result/videos/video

let $besthorrorsondvd := for $video in $videos
order by $video/user_rating descending
return $video[dvd and genre = "horror"]/title
return $besthorrorsondvd[1]