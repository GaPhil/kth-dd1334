(:6. Which actors have starred in a PG-13 movie between 1997 and 2006 (including1997 and 2006)?:)

let $videos := doc("videos.xml")/result/videos/video
let $actors2 := doc("videos.xml")/result/actors

let $actor_refs :=
    for $video in $videos
    where $video/rating = "PG-13" and $video/year >= 1997 and $video/year <= 2006
    return $video/actorRef

let $actors_with_names := distinct-values(
        for $actorref in $actor_refs
        return $actors2/actor[@id = $actorref])
return $actors_with_names
