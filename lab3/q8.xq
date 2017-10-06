(:8. Which director have the highest sum of user ratings?:)

(let $s := doc("videos.xml")
for $directors in distinct-values($s/result/videos/video/director)
let $director := $s/result/videos/video/director[. = $directors]
let $sum := sum(
        for $ratings in $s/result/videos/video
        where data($ratings/director) = data($director)
        return sum($ratings/user_rating))
order by $sum descending
return $director) [position() = 1]