import {
    GET_FIELD,
} from "../actions/field.actions";

const initialState = {};

export default function fieldReducer(state = initialState, action) {
  switch (action.type) {
    case GET_FIELD:
      return action.payload;
    default:
      return state;
  }
}
