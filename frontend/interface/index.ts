interface IGenre {
  id: number;
  title: string;
}

interface ICrew {
  id: number;
  fname: string;
  mname: string;
  lname: string;
  img: string;
  popular: number;
}

interface ITrialer {
  id: string;
}

interface IMovie {
  actors?: ICrew[];
  directors?: ICrew[];
  writers?: ICrew[];
  genres?: IGenre[];
  id: number;
  img_url: string;
  overview: string;
  popular: number;
  rating: number;
  release_date: Date;
  title: string;
  trailer?: ITrialer[];
}

interface IUser {
  display_name: string;
  username: string;
  password: string;
  email: string;
}

interface IComment {
  content: string;
  timestamp: string;
  user_id: string;
  displayName: string;
  img_url: string;
  like_count: number;
  comment_id: number;
  movieId: number;
  userId: string;
}

interface IList {
  favour_id: number;
  movie_id: number;
  movie_title: string;
  movie_release_date: string;
  user_id: string;
}
