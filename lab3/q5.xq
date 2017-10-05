(:5. Which is one of the highest rating movie starring both Brad Pitt and Morgan Freeman?:)

let $videos := doc("videos.xml")/result/videos/video
let $brad_id := doc("videos.xml")/result/actors/actor[. = "Pitt, Brad"]/@id
let $morgan_id := doc("videos.xml")/result/actors/actor[. = "Freeman, Morgan"]/@id

let $movies_with_actors :=
    for $video in $videos
    order by $video/user_rating descending
    return $video[actorRef = $brad_id and actorRef = $morgan_id]/title

return $movies_with_actors