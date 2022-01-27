import axios from "axios";

export const GET_FIELD = "GET_FIELD";

export const getField = () => {
    return (dispatch) => {
      return axios
        .get(`${process.env.REACT_APP_API_URL}api/field`)
        .then((res) => {
          dispatch({ type: GET_FIELD, payload: res.data });
        })
        .catch((err) => console.log(err));
    };
};